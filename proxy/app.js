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

const __dirname = path.dirname(import.meta.url);
dotenv.config();

const electronURL = process.env.ELECTRON_URL;
const loginUser = process.env.LOGIN_USER;
const loginPass = process.env.LOGIN_PASS;

const app = express();

app.use(cors({
    origin: electronURL,
    methods: ['GET', 'POST', 'OPTIONS'],
    allowedHeaders: ['Content-Type','Authorization']
  })
);
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(logger('dev'));
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

app.post('/auth/login', (req, res) => {
    const { username, password } = req.body;
    if (username === loginUser && password === loginPass) {
        const token = jwt.sign({ sub: username }, process.env.JWT_SECRET, {
            expiresIn: '15m',
        });
        return res.json({ token });
    }
    res.status(401).json({ error: 'Unauthorized' });
});

app.get('/api/data', async (req, res) => {
    console.log('🔍 Authorization header:', req.get('authorization'));
    const auth = req.headers.authorization;
    if (!auth?.startsWith('Bearer ')) return res.sendStatus(401);
    try {
        jwt.verify(auth.split(' ')[1], process.env.JWT_SECRET);
    } catch {
        return res.sendStatus(401);
    }
    try {
        const third = await axios.get('https://third.party/api/endpoint', {
            headers: { 'DEV_KEY': process.env.THIRD_PARTY_API_KEY },
        });
        return res.json(third.data);
    } catch (err) {
        return res.sendStatus(502).json({ error: 'Internal Server Error' });
    }
});

const PORT = process.env.PROXY_PORT;
app.listen(PORT, () => console.log(`Backend listening on port ${PORT}`));

export default app;
