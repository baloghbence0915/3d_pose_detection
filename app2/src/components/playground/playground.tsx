import ConfigPanel from '../config-panel/config-panel';
import PointsPreview from '../points-preview/points-preview';

export default function Playground() {
    return <>
        <PointsPreview />
        <ConfigPanel mode="threejs" />
    </>;
}
