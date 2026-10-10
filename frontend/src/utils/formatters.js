export function capitalizeFirst(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function formatDietType(dietType) {
  const map = {
    vegetarian: 'Vegetarian',
    eggitarian: 'Egg-Friendly',
    non_vegetarian: 'Non-Vegetarian',
    jain: 'Jain / Satvik'
  };
  return map[dietType] || capitalizeFirst(dietType);
}

export function formatFlowIntensity(flow) {
  const map = {
    spotting: 'Spotting',
    light: 'Light Flow',
    medium: 'Medium Flow',
    heavy: 'Heavy Flow'
  };
  return map[flow] || capitalizeFirst(flow);
}
