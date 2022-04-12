const fs = require('fs');
const {
    getSlidingAveraged,
    filterAngles,
    getPeaks,
    transformDomain,
    writeData,
    getCrosses,
} = require('./utils');
let data = fs.readFileSync('f1.csv', 'utf8')

const left1 = [];
const right1 = [];

data.split('\n')
    .forEach(d => {
        const angles = d.split(',').map(n => Number(n))
        left1.push(angles[0])
        right1.push(angles[1])
    });

const leftMagnitude2 =
    getSlidingAveraged(
        left1
            .map(filterAngles)
            .map(transformDomain)
        ,
        3
    )

const rightMagnitude2 =
    getSlidingAveraged(
        right1
            .map(filterAngles)
            .map(transformDomain)
        ,
        3
    )

const crosses3 = getCrosses(leftMagnitude2, rightMagnitude2)

const leftPeak3 = getPeaks(leftMagnitude2, 4)
const rightPeak3 = getPeaks(rightMagnitude2, 4)

let v = 0
let h = 0
const a = -1 / 200
let i = 0
const crosses3Copy = [...crosses3];
const width = 20
const result = Array(leftMagnitude2.length).fill(0).reduce((p, c) => {
    const quota = crosses3Copy.findIndex((vv, ii) => ii <= i && ii > i - width && vv !== 0);

    if (quota !== -1) {
        const leftPeak = leftPeak3[i] || 0
        const rightPeak = rightPeak3[i] || 0
        const peak = (leftPeak + rightPeak) / 2
        if (peak > 0) {
            if (h < (peak*12)) {
                v = 0
                h = peak * 10
                crosses3Copy[quota] = 0
            }
        }
    }

    v += a
    h += v
    if (h < 0) {
        h = 0
        v = 0
    } 
    i++
    return [...p, h / 3];
}, [])

fs.writeFileSync('f.csv',
    'id,label,value' +
    writeData(left1, 'left1') +
    writeData(right1, 'right1') +
    // writeData(leftMagnitude2, 'leftMagnitude2') +
    // writeData(rightMagnitude2, 'rigthMagnitude2') +
    // writeData(result, 'result') +
    '',
    'utf8')
