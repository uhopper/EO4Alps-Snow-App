//VERSION=3

// js file
function setup() {
  return {
    input: ["Snowdepth", "dataMask"],
    output: { bands: 4 },
    mosaicking: "TILE"}
}

function evaluatePixel(samples, scenes) {

  for (let i = 0; i < samples.length; i++){
    var tile = samples[i]
    // if there is 0 Snowdepth then return blank pixels.
    if (tile.dataMask == 1){
      if (tile.Snowdepth < 10){
        return [0,0,0,0]
      }
      else if (tile.Snowdepth < 20) {
        return [1,1,1,0.25]
      }
      else if (tile.Snowdepth < 30) {
        return [1,1,1,0.5]
      }
      else if (tile.Snowdepth < 40) {
        return [1,1,1,0.75]
      }
      else {
        return [1,1,1,1]
      }
    }
  }
  return [0,0,0,0]
}