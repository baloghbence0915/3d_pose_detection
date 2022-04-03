import { Config } from '../../types/config';
import { BehaviorSubject, debounce, interval } from 'rxjs';
import { DEFAULT_CONNECTION_URL } from './url';
import { Points } from '../../types/points';

export class ConnectionService {
    private static instance: ConnectionService;
    private host: string = '';
    public isConnected$: BehaviorSubject<boolean>;
    private keyPointStream: EventSource | null;
    private point$: BehaviorSubject<Points>;

    private constructor() {
        this.isConnected$ = new BehaviorSubject<boolean>(false);
        this.keyPointStream = null;
        this.point$ = new BehaviorSubject<Points>({ points: {}, angle: 0, speed: 0 });
    }

    public static getInstance(host: string = DEFAULT_CONNECTION_URL) {
        if (!this.instance) {
            this.instance = new ConnectionService();
        }

        this.instance.host = host;

        return this.instance;
    }

    public async startConntection(): Promise<ConnectionService> {
        const success = await fetch(`http://${this.host}/api`)
            .then(r => r.status === 200)
            .catch(() => false);

        if (success) {
            this.isConnected$.next(true);
        }
        return this;
    }

    public stopConntection(): void {
        this.isConnected$.next(false);
    }

    public startKeyPoints(setKeyPoints: (k: Points) => any): void {
        const createStream = () => {
            const eventSource = new EventSource(`http://${this.host}/api/stream/keypoints`);

            eventSource.onopen = () => {
                eventSource.onmessage = (e)=> {
                    this.point$.next(JSON.parse(e.data));
                }
            };

            eventSource.onerror = (e) => {
                console.error(e);
                this.stopStreamingKeypoints();
            };

            return eventSource;
        };

        this.point$.subscribe(setKeyPoints);

        if (!this.keyPointStream) {
            this.keyPointStream = createStream();
        }
    }

    public stopStreamingKeypoints(): void {
        if (this.keyPointStream) {
            this.keyPointStream.close();
            this.keyPointStream = null;
        }
    }

    public async getRecordings(): Promise<string[]> {
        const response = await this.fetch('/api/recordings');
        return response.json()
    }

    public async getPoints(): Promise<Points> {
        const response = await this.fetch(`/api/points`).then(r => r.json());
        return response;
    }

    public async getConfig() {
        const response = await this.fetch('/api/config');
        return response.json()
    }

    public async setConfig(config: Config) {
        const response = await this.fetch(
            '/api/config',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(config)
            });

        return response.json()
    }

    public getHost(): string {
        return this.host;
    }

    private fetch(path: string, options: RequestInit = {}): Promise<Response> {
        return fetch(
            `http://${this.host}${path}`,
            {
                ...options,
                headers: {
                    ...options.headers,
                    'Connection': 'Keep-Alive'
                },
                mode: 'cors',
            }).catch(e => {
                this.stopConntection();
                return Promise.reject(e);
            });
    }
}
