import { app, BrowserWindow, session, net } from 'electron';
import axios, { AxiosInstance } from 'axios';
import dotenv from 'dotenv';
import https from 'https';
import fs from 'fs';
import path from 'path';

dotenv.config();
const proxyBASE = process.env.PROXY_BASE;
const loginUser = process.env.LOGIN_USER;
const loginPass = process.env.LOGIN_PASS;
const djangoURL = process.env.DJANGO_URL;
const electronBypass = process.env.ELECTRON_BYPASS;

const resPath = app.isPackaged ? process.resourcesPath : path.join(__dirname, "..");
const cerPath = path.join(resPath, "cer.pem");
const keyPath = path.join(resPath, "key.pem");
const httpsAgent = new https.Agent({
  cert: fs.readFileSync(cerPath),
  key: fs.readFileSync(keyPath),
});

app.whenReady().then(async () => {
  let outgo: AxiosInstance;
  try {
    outgo = axios.create({
      baseURL: proxyBASE,
      httpsAgent,
      timeout: 100000,
      headers: { 'Content-Type': 'application/json' },
    });
    const resp = await outgo.post('/login/', {
      username: loginUser,
      password: loginPass
    });
    const jwtToken = String(resp.data.token);

    const win = new BrowserWindow({
      fullscreen: true,
      webPreferences: {
        devTools: false,
        nodeIntegration: false,
        contextIsolation: true,
        sandbox: true,
        javascript: true,
        zoomFactor: 1.0,
      }
    });
    session.defaultSession.clearCache();
    session.defaultSession.webRequest.onBeforeSendHeaders(
      { urls: [`${djangoURL}`] },
      (details, callback) => {
        const headers = { ...details.requestHeaders };
        headers['Authorization'] = `Bearer ${jwtToken}`;
        headers['ElectronBypass'] = `${electronBypass}`;
        headers['Pragma'] = 'no-cache';
        headers['Cache-Control'] = 'no-cache, no-store, must-revalidate';
        callback({ requestHeaders: headers });
      }
    );
    await win.loadURL(`${djangoURL}`);
    } catch (err) {
      app.quit();
    }
});
app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
});
