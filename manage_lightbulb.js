const LIGHTBULB_CHANGE_PERIOD_SEC = 10; // in seconds
const TRIGGER_PERIOD_SEC = 10; // in seconds
const CHANGE_LIGHT_COUNT_LEVEL = Math.round(
  LIGHTBULB_CHANGE_PERIOD_SEC / TRIGGER_PERIOD_SEC
);
const REVERSED_BRIGHTNESS = true;

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

function desaturateColor(r, g, b) {
  const maxRGBval = Math.max(r, g, b);
  const minRGBval = Math.min(r, g, b);
  const difference = Math.abs(maxRGBval - minRGBval);

  const desaturationLvl = Math.min(0.5, difference / 255);

  const avg = (r + g + b) / 3;
  r = r + desaturationLvl * (avg - r);
  g = g + desaturationLvl * (avg - g);
  b = b + desaturationLvl * (avg - b);
  return [r, g, b];
}

let sumRed = context.get("sum_red") || 0;
let sumGreen = context.get("sum_green") || 0;
let sumBlue = context.get("sum_blue") || 0;
let sumClear = context.get("sum_clear") || 0;
let counter = context.get("counter") || 0;

const red = parseFloat(msg.payload["sensor.light_meter_red"]) || 0;
const green = parseFloat(msg.payload["sensor.light_meter_green"]) || 0;
const blue = parseFloat(msg.payload["sensor.light_meter_blue"]) || 0;
const clear = parseFloat(msg.payload["sensor.light_meter_clear"]) || 0;

sumRed += red;
sumGreen += green;
sumBlue += blue;
sumClear += clear;
counter += 1;

context.set("sum_red", sumRed);
context.set("sum_green", sumGreen);
context.set("sum_blue", sumBlue);
context.set("sum_clear", sumClear);
context.set("counter", counter);

if (counter < CHANGE_LIGHT_COUNT_LEVEL) {
  return;
}
const avgRed = sumRed / counter;
const avgGreen = sumGreen / counter;
const avgBlue = sumBlue / counter;
const avgClear = sumClear / counter;

context.set("sum_red", 0);
context.set("sum_green", 0);
context.set("sum_blue", 0);
context.set("sum_clear", 0);
context.set("counter", 0);

const total = avgRed + avgGreen + avgBlue;
const normalizedRed = total ? (avgRed / total) * 255 : 0;
const normalizedGreen = total ? (avgGreen / total) * 255 : 0;
const normalizedBlue = total ? (avgBlue / total) * 255 : 0;

const brightnessInPct = Math.min(Math.max((avgClear / 255) * 100, 0), 100);

const outputBrightness = REVERSED_BRIGHTNESS
  ? 100 - brightnessInPct
  : brightnessInPct;

const timeOfDay = getTimeOfDay();
let [adjustedRed, adjustedGreen, adjustedBlue] = adjustLightColor(
  normalizedRed,
  normalizedGreen,
  normalizedBlue,
  timeOfDay
);

[adjustedRed, adjustedGreen, adjustedBlue] = desaturateColor(
  adjustedRed,
  adjustedGreen,
  adjustedBlue
);

msg.payload = {
  entity_id: "light.living_room_light",
  rgb_color: [
    Math.round(Math.max(0, Math.min(255, adjustedRed))),
    Math.round(Math.max(0, Math.min(255, adjustedGreen))),
    Math.round(Math.max(0, Math.min(255, adjustedBlue))),
  ],
  brightness_pct: Math.round(Math.max(0, Math.min(100, outputBrightness))),
};

context.set("prev_red", adjustedRed);
context.set("prev_green", adjustedGreen);
context.set("prev_blue", adjustedBlue);
context.set("prev_brightness", outputBrightness);

return msg;
