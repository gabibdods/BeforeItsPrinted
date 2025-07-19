import {app, BrowserWindow, session} from 'electron';

app.whenReady().then(async () => {
    await session.defaultSession.clearCache();
    const token = "hopeitworks";
    const authentication = "electronconfirmed";

    session.defaultSession.webRequest.onBeforeSendHeaders((details: { requestHeaders: { [x: string]: string; }; }, callback: (arg0: { requestHeaders: any; }) => void) => {
        details.requestHeaders['DEV_KEY'] = token;
        details.requestHeaders['ELECTRON'] = authentication;
        callback({ requestHeaders: details.requestHeaders });
    });
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
    win.loadURL("http://127.0.0.1:9000/bip/");
    win.webContents.openDevTools({ mode: 'detach' });
});
app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
});
