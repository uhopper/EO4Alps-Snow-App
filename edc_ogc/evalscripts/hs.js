//VERSION=3

function setup() {
  return {
    input: ["Snowdepth", "dataMask"],
    output: { bands: 4 },
    mosaicking: "TILE"}
}

function evaluatePixel(samples, scenes) {

  for (let i = 0; i < samples.length; i++){
    var tile = samples[i]
      // if there is 0 SWE then return blank pixels.
    if (tile.dataMask == 1){
      if (tile.Snowdepth == 0){
        return [0,0,0,0]
      }
      // if it is no data -9999 then return blank pixels.
        else if (tile.Snowdepth == -9999){
          return [0,0,0,0]
        }
        else if (tile.Snowdepth > 2500){
          return [1,0,0,tile.dataMask]
        }
        else if (tile.Snowdepth > 2000){
          return [0.6,0.4,0.2,tile.dataMask]
        }
        else if (tile.Snowdepth > 1600){
          return [1,0.45,0,tile.dataMask]
        }
        else if (tile.Snowdepth > 1200){
          return [0.94,0,1,tile.dataMask]
        }
        else if (tile.Snowdepth > 1000){
          return [0.5,0,0.5,tile.dataMask]
        }
        else if (tile.Snowdepth > 800){
          return [0,0,0.59,tile.dataMask]
        }
        else if (tile.Snowdepth > 600){
          return [0,0.47,1,tile.dataMask]
        }
        else if (tile.Snowdepth > 400){
          return [0,1,1,tile.dataMask]
        }
        else if (tile.Snowdepth > 200){
          return [0.11,0.83,0.03,tile.dataMask]
        }
        else if (tile.Snowdepth > 100){
          return [0.6,1,0.51,tile.dataMask]
        }
        else if (tile.Snowdepth > 50){
          return [1,0.87,0.18,tile.dataMask]
        }
        else if (tile.Snowdepth > 20){
          return [1,1,0.68,tile.dataMask]
        }
        else if (tile.Snowdepth > 1){
          return [1,1,1,0.5]
        }
        else{
        return [0,0,0,0]
      }
    }
  }
  return [0,0,0,0]
}