import ThreeStats from 'three/examples/jsm/libs/stats.module';

export class StatsService {
    private static instance: StatsService;

    private constructor(private stats: ThreeStats) { }

    public static getInstance() {
        if (!this.instance) {
            this.instance = new StatsService(ThreeStats());
        }
        return this.instance;
    }

    public update() {
        this.stats.update();
    }

    public getStatsObject() {
        return this.stats;
    }
}
