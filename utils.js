exports.getSlidingAveraged = function (arr, width) {
    const newArray = []

    const slidingAvg = (arr, c) => {
        const arr2 = [...arr.slice(Math.max(arr.length - width, 0)), c];
        const avg = arr2.reduce((p, c) => c + p, 0) / arr2.length
        newArray.push(avg)

        return [...arr, c]
    }

    arr.reduce(slidingAvg, [])

    return newArray
}


exports.getPeaks = function (arr, width) {
    let mode = 'down'
    let peak = 0
    const peaks = [];

    function _processPeaks(arr, c) {
        peaks.push(undefined)
        let hasChanged = false

        if (mode === 'down') {
            if (isUp(arr, c)) {
                mode = 'up';
                hasChanged = true
            }
        }

        if (mode === 'up') {
            if (c > peak) {
                peak = c
            }
            if (isDown(arr, c) && !hasChanged) {
                mode = 'down';
                peaks[peaks.length - 1] = peak
                peak = 0
            }
        }
    }

    function isUp(arr, c) {
        const arr2 = [...arr.slice(Math.max(arr.length - width - 1, 0)), c];
        const avg = arr2.reduce((p, c) => p + c, 0) / arr2.length;
        return avg < arr2[arr2.length - 1]
    }

    function isDown(arr, c) {
        const arr2 = [...arr.slice(Math.max(arr.length - width + 1, 0)), c];
        const avg = arr2.reduce((p, c) => p + c, 0) / arr2.length;
        return avg < arr2[0]
    }


    arr.reduce((p, c) => {
        _processPeaks(p, c)
        return [...p, c]
    }, [])

    peaks[0] = 0

    return peaks
}


exports.filterAngles = function (v) {
    const filterThreshold = 0.1; // ~5-6°
    return v > filterThreshold ? v : 0
}

exports.transformDomain = function (v) {
    return v / Math.PI
}

// exports.getDerivative = function (arr) {
//     let prev = 0;
//     return arr.reduce((arr, c) => {
//         const res = [...arr, c - prev]
//         prev = c;
//         return res
//     }, [])
// }

// exports.transformDerivate = function (v) {
//     return v > 0 ? 1 : (v < 0 ? -1 : 0)
// }


exportsgetProcessedPeaks = function (peakArray, width) {
    const procPeakArray = Array(width - 1).fill(0);
    for (let i = width; i <= peakArray.length; i++) {
        const arr = peakArray.slice(i - width, i)
        let n = 0;
        const sum = arr.reduce((p, c) => {
            if (c > 0)
                n++
            return p + c;
        }, 0);
        procPeakArray.push(n === 0 ? 0 : sum / n);
    }
    return procPeakArray
}

// exports.multiplyArrays = function (peaks1, peaks2) {
//     const combinedPeaks = [];
//     for (let i = 0; i < peaks1.length; i++) {
//         combinedPeaks.push(peaks1[i] * peaks2[i] * 1)
//     }
//     return combinedPeaks
// }

exports.writeData = function (arr, label) {
    return '\n' + arr.map((d, i) => d === undefined ? '' : `${i},${label},${d}`).join('\n')
}

// exports.getFrequency = function (arr, width) {
//     const frequency = []

//     arr.reduce((arr2, c) => {
//         const arr3 = [...arr2.slice(Math.max(arr2.length - width + 1, 0)), c];
//         const count = arr3.reduce((c, current) => current !== undefined ? c + 0.1 : c, 0)
//         frequency.push(count)
//         return [...arr2, c];
//     }, []);

//     return frequency
// }

// exports.getFrequency2 = function (arr, width) {
//     const frequency = []

//     arr.reduce((arr2, c) => {
//         frequency.push(0)
//         const arr3 = [...arr2.slice(Math.max(arr2.length - width + 1, 0)), c];
//         const count = arr3.find(v => v > 0)
//         if(count)
//             frequency[frequency.length - 1] = 0.3
//         return [...arr2, c];
//     }, []);

//     return frequency
// }

exports.getCrosses = function (der1, der2) {
    const changing = []

    function isCrossing(p1, p2, c1, c2) {
        if (p1 !== undefined && p2 !== undefined) {
            const isInc1 = p1 < c1
            const isInc2 = p2 < c2
            let a
            let b

            if (isInc1 && !isInc2) {
                a = { p: p2, c: c2 }
                b = { p: p1, c: c1 }
            } else if (!isInc1 && isInc2) {
                a = { p: p1, c: c1 }
                b = { p: p2, c: c2 }
            } else {
                return false
            }

            return (b.c < a.p && b.c > a.c) || (b.p < a.p && b.p > a.c) || (b.p < a.p && b.c > a.c)
        }
        return false
    }

    for (let i = 0; i < der1.length; i++) {
        changing.push(0)
        const prev1 = der1[i - 1]
        const prev2 = der2[i - 1]
        const curr1 = der1[i]
        const curr2 = der2[i]

        if (isCrossing(prev1, prev2, curr1, curr2)) {
            changing[changing.length - 1] = 0.2
        }
    }

    changing[0] = 0

    return changing
}
