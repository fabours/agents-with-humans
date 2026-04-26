export async function getCurrentWeather(city) {
  const response = await fetch(`/api/weather/current?city=${encodeURIComponent(city)}`)
  if (!response.ok) throw new Error(`Weather API error: ${response.status}`)
  return response.json()
}
