import express from 'express';
import path from 'path';
import cors from 'cors';
import dotenv from 'dotenv';
import cookieParser from 'cookie-parser';
import jwt from 'jsonwebtoken';
import axios from 'axios';
import logger from 'morgan';
import { createProxyMiddleware } from 'http-proxy-middleware';

import indexRouter from './routes/index.js';
import usersRouter from './routes/users.js';

import { fileURLToPath } from 'url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));

const corsORIGINS = process.env.CORS_ORIGINS;
const loginUser = process.env.LOGIN_USER;
const loginPass = process.env.LOGIN_PASS;
const jwtSecret = process.env.JWT_SECRET;
const thirdPartyAPIKey = process.env.THIRD_PARTY_API_KEY;
const electronBypass = process.env.ELECTRON_BYPASS;

const app = express();

app.use(cors({
    origin: corsORIGINS,
    methods: ['GET', 'POST'],
    allowedHeaders: "*",
  })
);
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(logger('dev'));
app.use(express.static(path.join(__dirname, 'public')));

app.set('trust-proxy', 1);

app.use('/', indexRouter);
app.use('/users/', usersRouter);

app.get('/bip/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'main.html'));
});

app.use('/bip/parse/', createProxyMiddleware({
  target: 'http://bipfa:9000/parse/',
  changeOrigin: true,
  ws: false,
  pathRewrite: { '^/parse/': '/parse/' }
}));

app.post('/login/', (req, res) => {
    const { username, password } = req.body;
    if (username === loginUser && password === loginPass) {
        const token = jwt.sign({ sub: username }, jwtSecret, {
            expiresIn: '5m',
        });
        return res.json({ token });
    }
    res.status(401).json({ error: 'Login Failed' });
});

app.get('/token/', async (req, res) => {
    const auth = req.headers.authorization;
    if (!auth?.startsWith('Bearer ')) return res.sendStatus(401);
    try {
        jwt.verify(auth.split(' ')[1], jwtSecret);
    } catch {
        return res.sendStatus(403);
    }
    try {
        const third = await axios.get('https://third.party/api/endpoint', {
            headers: { 'DEV_KEY': thirdPartyAPIKey },
        });
        return res.json(third.data);
    } catch (err) {
        return res.status(502).json({ error: 'Authorization Uncompleted' });
    }
});

app.listen(3000);

export default app;
