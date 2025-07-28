import {app, BrowserWindow, session, net} from 'electron';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const djangoURL = process.env.DJANGO_URL;
const fastAPIURL = process.env.FASTAPI_URL;
const proxyURL = process.env.PROXY_URL;
const loginUser = process.env.LOGIN_USER;
const loginPass = process.env.LOGIN_PASS;
const electronBypass = process.env.ELECTRON_BYPASS;

let jwtToken: string;

async function loginProxy() {
    const resp = await axios.post(`${proxyURL}/auth/login`, {
        username: loginUser, password: loginPass
    });
    jwtToken = resp.data.token
    axios.defaults.baseURL = proxyURL;
    axios.defaults.headers.common['Authorization'] = `Bearer ${jwtToken}`;
}
function attachAuthHeader() {
    const filter = {
        urls: [
            `${fastAPIURL}/*`,
            `${djangoURL}/*`,
        ],
    };
    session.defaultSession.webRequest.onBeforeSendHeaders(filter, (details, callback) => {
        if (jwtToken) {
            details.requestHeaders['Authorization'] = `Bearer ${jwtToken}`;
        }
        details.requestHeaders['ElectronBypass'] = `${electronBypass}`;
        callback({ requestHeaders: details.requestHeaders });
    });
}
function loginDjango(): Promise<void> {
    return new Promise((resolve, reject) => {
        const req = net.request({
            method: 'GET',
            url: `${djangoURL}/bip/`,
            session: session.defaultSession,
            headers: {
                'Content-Type': 'application/json',
            },
        });
        req.on('response', (response) => {
            if (response.statusCode === 201) {
                resolve();
            } else {
                reject(new Error(`Django Login Failed: ${response.statusCode} ${response.statusMessage}`));
            }
        });
        req.on('error', reject);

        req.write(JSON.stringify({ username: loginUser, password: loginPass }));
        req.end();
    });
}
async function createWindow() {
    const win = new BrowserWindow({
        fullscreen: true,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            sandbox: true,
            javascript: true,
            zoomFactor: 1.0,
        }
    });
    await win.loadURL(`${djangoURL}/bip/`);
    //win.webContents.openDevTools({ mode: 'detach' });
}
app.whenReady().then(async () => {
    try {
        await loginProxy();
        attachAuthHeader();
        await loginDjango();
        await createWindow();
    } catch (err) {
        console.error(err);
        app.quit();
    }
});
app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
});
