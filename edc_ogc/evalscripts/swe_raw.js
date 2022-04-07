//VERSION=3

function setup() {
  return {
    input: [{
        bands: ["SWE"]
    }],
    output: {
        bands: 1,
        sampleType: SampleType.FLOAT32
    },
  }
}

function evaluatePixel(sample) {
    return [sample.SWE];
}
