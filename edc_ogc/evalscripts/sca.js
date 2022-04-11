//VERSION=3

function setup() {
  return {
    input: ["s2snow", "dataMask"],
    output: { bands: 4 },
    mosaicking: "ORBIT"}
}

function evaluatePixel(samples, scenes) {

  for (let i = 0; i < samples.length; i++){
    var tile = samples[i]
      // if there is 0 SWE then return blank pixels.
    if (tile.dataMask == 1){
      if (tile.s2snow == 0){
        return [0,0,0,0]
      }
      // if it's no data -9999 then return blank pixels.
        else if (tile.s2snow == 0){
          return [0,0,0,tile.dataMask]
        }
        else if (tile.s2snow == 1){
          return [1,1,1,tile.dataMask]
        }
        else if (tile.s2snow == 2){
          return [0,0.6,0.3,tile.dataMask]
        }
        else if (tile.s2snow == 3){
          return [0.5,0.5,0.5,tile.dataMask]
        }
        else if (tile.s2snow == 4){
          return [0,0.5,1,tile.dataMask]
        }
        else if (tile.s2snow == 255){
          return [0,0,0,0]
        }
        else{
        return [0,0,0,0]
      }
    }
  }
}