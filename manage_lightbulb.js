const MIN_RGB = [255, 201, 100];
const MAX_RGB = [255, 255, 255];
const LIGHTBULB_CHANGE_PERIOD_SEC = 60; // in seconds
const TRIGGER_PERIOD_SEC = 10; // in seconds
const CHANGE_LIGHT_COUNT_LEVEL = Math.round(LIGHTBULB_CHANGE_PERIOD_SEC / TRIGGER_PERIOD_SEC);
const REVERSED_BRIGHTNESS = true;

function calculateSinRGB(currentTime, sunrise, sunset) {
    const dayLength = sunset - sunrise;
    const timeSinceSunrise = currentTime - sunrise;

    const scale = Math.min(Math.max(1.5 * Math.sin((timeSinceSunrise / dayLength) * 0.9 * Math.PI) + 0.3, 0), 1)

    const r = MIN_RGB[0] + scale * (MAX_RGB[0] - MIN_RGB[0]);
    const g = MIN_RGB[1] + scale * (MAX_RGB[1] - MIN_RGB[1]);
    const b = MIN_RGB[2] + scale * (MAX_RGB[2] - MIN_RGB[2]);

    return [Math.round(r), Math.round(g), Math.round(b)];
}

let sumClear = context.get('sum_clear') || 0;
let counter = context.get('counter') || 0;

const clear = parseFloat(msg.payload["sensor.light_meter_clear"]) || 0;

sumClear += clear;
counter += 1;
context.set('sum_clear', sumClear);
context.set('counter', counter);

if (counter < CHANGE_LIGHT_COUNT_LEVEL) {
    return;
}
const avgClear = sumClear / counter;

context.set('sum_clear', 0);
context.set('counter', 0);

const brightnessInPct = Math.min(Math.max((avgClear / 255) * 100, 0), 100);

const outputBrightness = REVERSED_BRIGHTNESS ? (100 - brightnessInPct) : brightnessInPct;
context.set('prev_brightness', outputBrightness);

const sunrise_ISO_8601 = flow.get('sunrise');
const sunrise = new Date(sunrise_ISO_8601);
const sunset_ISO_8601 = flow.get('sunset');
const sunset = new Date(sunset_ISO_8601);
node.warn('Sunrise: ' + sunrise);
node.warn('Sunset: ' + sunset);

const today = new Date();
const year = today.getFullYear();
const month = today.getMonth();
const date = today.getDate();
const currentTime = new Date(year, month, date, 13, 0, 0, 0);
node.warn('Current time: ' + currentTime);

const [adjustedRed, adjustedGreen, adjustedBlue] = calculateSinRGB(currentTime, sunrise, sunset);

msg.payload = {
    entity_id: "light.living_room_light",
    rgb_color: [
        adjustedRed,
        adjustedGreen,
        adjustedBlue
    ],
    brightness_pct: Math.round(Math.max(0, Math.min(100, outputBrightness)))
};

return msg;