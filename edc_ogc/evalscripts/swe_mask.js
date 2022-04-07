//VERSION=3

// js file
function setup() {
  return {
    input: ["SWE", "dataMask"],
    output: { bands: 4 },
    mosaicking: "TILE"}
}

function evaluatePixel(samples, scenes) {

  for (let i = 0; i < samples.length; i++){
    var tile = samples[i]
    // if there is 0 SWE then return blank pixels.
    if (tile.dataMask == 1){
      if (tile.SWE < 5){
        return [0,0,0,0]
      }
      else if (tile.SWE < 10) {
        return [0.9,1,1,0.25]
      }
      else if (tile.SWE < 15) {
        return [0.9,1,1,0.5]
      }
      else if (tile.SWE < 20) {
        return [0.9,1,1,0.75]
      }
      else {
        return [0.9,1,1,1]
      }
    }
  }
  return [0,0,0,0]
}