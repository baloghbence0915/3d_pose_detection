const fs = require('fs')
const offset = 0.075;

let data = fs.readFileSync('f1.csv', 'utf8')

data = data
    .split('\n')
    .map(
        l => [...l.split(',').map(n => Number(n)), 0, 0]
        // .map((ll, i) => i === 0 ? `left,${ll}` : `right,${ll}`)
    );

function slidingAvg(arr, c, step) {
    let arr2 = [
        ...arr.slice(Math.max(arr.length - step, 0)),
        c
    ];
    const l = arr2.length;

    arr2 = arr2.reduce((p, c) => [c[0] + p[0], c[1] + p[1], 0, 0], [0, 0, 0, 0])
    arr2[0] /= l
    arr2[1] /= l

    return arr2;
}

let peakRightArray = [];
let peakLeftArray = [];

class SWindow {

    constructor(width, side, peakArray) {
        this.width = width - 1
        this.mode = 'down'
        this.peak = 0
        this.peakArray = peakArray
        this.side = side === 'left' ? 0 : 1
    }

    processPeak(arr, c) {
        this.peakArray.push(0)

        if (this.mode === 'down') {
            if (this.isUp(arr, c)) {
                this.mode = 'up';
            }
        }

        if (this.mode === 'up') {
            let peak = 0
            if (c[this.side] > this.peak) {
                this.peak = c[this.side]
                peak = c[this.side]
            }

            if (this.isDown(arr, c)) {
                this.mode = 'down';
                peak = this.peak
                this.peakArray[this.peakArray.length - 1] = this.peak
                this.peak = 0
                // return peak
            }
            // return peak > 0 ? peak : undefined
        }
    }

    isUp(arr, c) {
        const arr2 = [...arr.slice(Math.max(arr.length - (this.width), 0)), c];
        const avg = arr2.reduce((p, c) => p + c[this.side], 0) / arr2.length;
        return avg < arr2[arr2.length - 1][this.side]
    }

    isDown(arr, c) {
        const arr2 = [...arr.slice(Math.max(arr.length - (this.width), 0)), c];
        const avg = arr2.reduce((p, c) => p + c[this.side], 0) / arr2.length;
        return avg < arr2[0][this.side]
    }
}

const leftSwindow = new SWindow(4, 'left', peakLeftArray)
const rightSwindow = new SWindow(4, 'right', peakRightArray)

data = data
    .reduce((p, c) =>
        [
            ...p,
            slidingAvg(p, c, 1)
        ], [])
    .map(l => l.map(n => n > offset ? n - offset : 0))
    // [left, right, leftDer, rightDer]
    .reduce((p, c) =>
        [
            ...p,
            [
                c[0],
                c[1],
                0,
                // p[p.length - 1] ? c[0] - p[p.length - 1][0] : 0,
                0,
                // p[p.length - 1] ? c[1] - p[p.length - 1][1] : 0,
            ]
        ],
        []);

data.reduce((p, c) => {
    leftSwindow.processPeak(p, c)
    rightSwindow.processPeak(p, c)
    return [
        ...p,
        c,
    ];
}, []);

// console.log(data);

// data = data.map((l, i) => `${i},left,${l[0]}\n${i},leftDer,${l[2]}\n${i},right,${l[1]}\n${i},rightDer,${l[3]}`)



function getProcPeaks(peakArray, width, gap) {
    const procPeakArray = Array(width - 1).fill(0);

    for (let i = width; i <= peakArray.length; i++) {
        if (i % gap === 0) {

            const arr = peakArray.slice(i - width, i)
            let n = 0;
            const sum = arr.reduce((p, c) => {
                if (c === undefined)
                    return p

                if (c > 0)
                    n++
                return p + c;
            }, 0);
            procPeakArray.push(n === 0 ? 0 : sum / n);
        } else {
            procPeakArray.push(undefined);
        }
    }

    return procPeakArray
}

function splitPeaks(peakArray, gap) {
    const newPeakArray = Array.from(peakArray)

    function _splitPeaks(startIdx, endIdx) {
        const from = newPeakArray[startIdx]
        const to = newPeakArray[endIdx]
        const step = (to - from) / ((endIdx - startIdx) / gap)
        let prevValue = newPeakArray[startIdx]
        for (let i = startIdx + 1; i < endIdx; i++) {
            if (i % gap === 0) {
                newPeakArray[i] = prevValue + step
                prevValue = newPeakArray[i]
            } else {
                newPeakArray[i] = undefined
            }
        }
    }

    let startIdx = 0;
    for (let i = 0; i < newPeakArray.length; i++) {
        if (newPeakArray[i] > 0 && (i - startIdx) > 1) {
            _splitPeaks(startIdx, i)
            startIdx = i
        }
    }

    return newPeakArray
}

const gap = 4
const leftSplitPeaks = splitPeaks(peakLeftArray, gap)
const leftProcessedPeak = getProcPeaks(leftSplitPeaks, 30, gap);
const rightSplitPeaks = splitPeaks(peakRightArray, gap)
const rightProcessedPeak = getProcPeaks(rightSplitPeaks, 30, gap);

function combinePeaks(peaks1, peaks2) {
    const combinedPeaks = [];

    for (let i = 0; i < peaks1.length; i++) {
        if (peaks1[i] === undefined || peaks2[i] === undefined) {
            combinedPeaks.push(0)
        } else {
            combinedPeaks.push(peaks1[i] * peaks2[i] * 5)
        }
    }

    return splitPeaks(combinedPeaks, 4)
}

fs.writeFileSync('f4.csv',
    'id,label,value\n' +
    data.map((l, i) =>
        // `${i},left,${l[0]}\n` +
        // `${i},right,${l[1]}`
        ''
    ).join('\n') +
    '\n' + peakRightArray.map((p, i) => `${i},rightPeak,${p}`).join('\n') +
    '\n' + rightSplitPeaks.map((p, i) => p === undefined ? undefined : `${i},rightSplitPeak,${p}`).filter(Boolean).join('\n') +
    '\n' + rightProcessedPeak.map((p, i) => p === undefined ? undefined : `${i},rightProcPeak,${p}`).filter(Boolean).join('\n') + 
    '\n' + peakLeftArray.map((p, i) => `${i},leftPeak,${p}`).join('\n') +
    '\n' + leftSplitPeaks.map((p, i) => p === undefined ? undefined : `${i},leftSplitPeak,${p}`).filter(Boolean).join('\n') +
    '\n' + leftProcessedPeak.map((p, i) => p === undefined ? undefined : `${i},leftProcPeak,${p}`).filter(Boolean).join('\n') + 
    '\n' + combinePeaks(rightProcessedPeak, leftProcessedPeak).map((p, i) => p === undefined ? undefined : `${i},combinedPeak,${p}`).join('\n'),
    'utf8')

// console.log(getProcPeaks([0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0], 4));