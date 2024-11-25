function getTimeOfDay() {
  const currentHour = new Date().getHours();
  if (currentHour >= 6 && currentHour < 12) {
    return "morning";
  } else if (currentHour >= 12 && currentHour < 18) {
    return "day";
  } else if (currentHour >= 18 && currentHour < 22) {
    return "evening";
  } else {
    return "night";
  }
}

function adjustLightColor(r, g, b, timeOfDay) {
  switch (timeOfDay) {
    case "morning":
      r = Math.min(255, Math.round(r * 1.2));
      g = Math.min(255, Math.round(g * 1.0));
      b = Math.min(255, Math.round(b * 0.8));
      break;
    case "day":
      r = Math.min(255, Math.round(r * 1.0));
      g = Math.min(255, Math.round(g * 1.0));
      b = Math.min(255, Math.round(b * 1.0));
      break;
    case "evening":
      r = Math.min(255, Math.round(r * 1.3));
      g = Math.min(255, Math.round(g * 1.1));
      b = Math.min(255, Math.round(b * 0.7));
      break;
    case "night":
      r = Math.min(255, Math.round(r * 1.5));
      g = Math.min(255, Math.round(g * 1.2));
      b = Math.min(255, Math.round(b * 0.5));
      break;
  }
  return [r, g, b];
}

// Get the RGB values
const red = parseFloat(msg.payload["sensor.light_meter_red"]) || 0;
const green = parseFloat(msg.payload["sensor.light_meter_green"]) || 0;
const blue = parseFloat(msg.payload["sensor.light_meter_blue"]) || 0;
const clear = parseFloat(msg.payload["sensor.light_meter_clear"]) || 0;

// Debug log to check input values
// node.warn(`Red: ${red}, Green: ${green}, Blue: ${blue}, Clear: ${clear}`);

// Normalize RGB values
const total = red + green + blue;
const normalizedRed = total ? (red / total) * 255 : 0;
const normalizedGreen = total ? (green / total) * 255 : 0;
const normalizedBlue = total ? (blue / total) * 255 : 0;

// Normalize brightness % (Ensure value is between 0 and 100)
const brightnessPct = Math.min(Math.max((clear / 255) * 100, 0), 100);

// Debug log to check normalized values
node.log(
  `Normalized Red: ${normalizedRed}, Normalized Green: ${normalizedGreen}, Normalized Blue: ${normalizedBlue}, Brightness (pct): ${brightnessPct}`
);

const timeOfDay = getTimeOfDay();

const [adjustedRed, adjustedGreen, adjustedBlue] = adjustLightColor(
  normalizedRed,
  normalizedGreen,
  normalizedBlue,
  timeOfDay
);

node.log(
  `Adjusted Red: ${adjustedRed}, Adjusted Green: ${adjustedGreen}, Adjusted Blue: ${adjustedBlue}, Brightness (pct): ${brightnessPct}`
);

msg.payload = {
  entity_id: "light.living_room_light",
  rgb_color: [adjustedRed, adjustedGreen, adjustedBlue],
  brightness_pct: Math.round(brightnessPct), // Use percentage for brightness
};

return msg;
