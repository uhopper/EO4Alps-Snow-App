//VERSION=3

function setup() {
  return {
    input: [{
        bands: ["Snowdepth"]
    }],
    output: {
        bands: 1,
        sampleType: SampleType.FLOAT32
    },
  }
}

function evaluatePixel(sample) {
    return [sample.Snowdepth];
}
