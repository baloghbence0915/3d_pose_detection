import { deserialize } from 'bson';
import { Config } from '../../types/config';
import { NOT_FOUND_PIC } from '../../not-found-pic';
import { BehaviorSubject } from 'rxjs';
import { DEFAULT_CONNECTION_URL } from './url';
import { Frames } from '../../types/frames';
import { Points } from '../../types/points';

export class ConnectionService {
    private static instance: ConnectionService;
    private host: string = '';
    public isConnected$: BehaviorSubject<boolean>;

    private constructor() {
        this.isConnected$ = new BehaviorSubject<boolean>(false);
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

    public async getConfig() {
        const response = await this.fetch('/api/config');
        return response.json()
    }

    public async getRecordings(): Promise<string[]> {
        const response = await this.fetch('/api/recordings');
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

    public async getFrames(): Promise<Frames> {
        let obj;
        try {
            const response = await this.fetch(`/api/frames`);
            const bson = await response.arrayBuffer();
            obj = deserialize(bson);    
        } catch {}

        return {
            left: { frame: this.getImageBase64(obj?.left?.frame), res: obj?.left?.res },
            right: { frame: this.getImageBase64(obj?.right?.frame), res: obj?.right?.res }
        };
    }

    public async getPoints(): Promise<Points> {
        const response = await this.fetch(`/api/points`).then(r => r.json());
        return response;
    }

    private async fetch(path: string, options: RequestInit = {}): Promise<Response> {
        if (this.isConnected$.value) {
            const resp = await fetch(
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
            
            if (resp.status >= 200 && resp.status < 300) {
                return resp;
            }

            this.stopConntection();
            return Promise.reject('Server is not connected');
        }

        return Promise.reject('Server is not connected');
    }

    private getImageBase64(img: Buffer): string {
        if (!img) {
            return NOT_FOUND_PIC;
        }

        return `data:image/jpeg;base64,${img.toString('base64')}`;
    }

    public getHost(): string {
        return this.host;
    }
}
