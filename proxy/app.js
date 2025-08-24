import express from 'express';
import path from 'path';
import cors from 'cors';
import dotenv from 'dotenv';
import cookieParser from 'cookie-parser';
import jwt from 'jsonwebtoken';
import axios from 'axios';
import logger from 'morgan';

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

app.use('/', indexRouter);
app.use('/users', usersRouter);

app.post('/login/', (req, res) => {
    console.log(req);
    const tokenTest = jwt.sign({ sub: "N@*4hmZn?q8}%8e" }, jwtSecret, { expiresIn: '5m' });
    return res.json({ tokenTest });

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
    console.log('Authorization header:', req.get('authorization'));
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
