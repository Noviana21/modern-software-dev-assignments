import httpx
import logging
import sys
from mcp.server.fastmcp import FastMCP

# Konfigurasi Logging: WAJIB pakai stderr agar tidak merusak komunikasi STDIO MCP
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(levelname)s: %(message)s')

# Inisialisasi server MCP
mcp = FastMCP("OpenMeteo-Server")

# ==========================================
# TOOL 1: get_current_weather
# ==========================================
@mcp.tool()
async def get_current_weather(latitude: float, longitude: float) -> str:
    """Mengambil suhu dan kondisi cuaca saat ini berdasarkan koordinat latitude dan longitude."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status() # Menangkap error jika API mati / limit
            
            data = response.json()
            current = data.get("current_weather")
            
            if not current:
                return "Data cuaca saat ini tidak ditemukan dari API."
                
            temp = current.get('temperature')
            wind = current.get('windspeed')
            return f"Cuaca saat ini di koordinat ({latitude}, {longitude}): Suhu {temp}°C, Kecepatan Angin {wind} km/h."
            
    except httpx.TimeoutException:
        logging.error("Timeout saat menghubungi Open-Meteo.")
        return "Error: Koneksi ke API cuaca terputus (Timeout)."
    except httpx.HTTPError as e:
        logging.error(f"HTTP Error: {e}")
        return f"Error saat mengambil data cuaca: {e}"
    except Exception as e:
        logging.error(f"Error tidak terduga: {e}")
        return "Terjadi kesalahan internal pada server saat mengambil cuaca."

# ==========================================
# TOOL 2: get_weather_forecast
# ==========================================
@mcp.tool()
async def get_weather_forecast(latitude: float, longitude: float, days: int = 3) -> str:
    """Mengambil prakiraan cuaca (suhu max/min) untuk beberapa hari ke depan (default 3 hari)."""
    # Membatasi maksimal 7 hari agar rapi
    if days > 7:
        days = 7
        
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days={days}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            
            data = response.json()
            daily = data.get("daily")
            
            if not daily:
                return "Data prakiraan cuaca tidak ditemukan."
                
            dates = daily.get("time", [])
            max_temps = daily.get("temperature_2m_max", [])
            min_temps = daily.get("temperature_2m_min", [])
            
            result = f"Prakiraan cuaca {days} hari ke depan untuk ({latitude}, {longitude}):\n"
            for i in range(len(dates)):
                result += f"- {dates[i]}: Min {min_temps[i]}°C, Max {max_temps[i]}°C\n"
                
            return result
            
    except Exception as e:
        logging.error(f"Error mengambil forecast: {e}")
        return "Gagal mengambil data prakiraan cuaca dari API."

# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":
    # Menjalankan server menggunakan standard input/output (STDIO)
    mcp.run(transport="stdio")