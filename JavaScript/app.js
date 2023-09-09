import createError from 'http-errors'
import dotenv from 'dotenv'
import express from 'express'
import logger from 'morgan'

// 從環境變數導入應用程式設定
dotenv.config()
const { env } = process
const config = {
    env: env.NODE_ENV,
    debug: env.DEBUG?.toLowerCase() === 'true' || false,
    port: Number(env.PORT),
    url: env.APP_URL ? env.APP_URL : `http://127.0.0.1:${Number(env.PORT)}`
}

// 實作 express
const app = express()
app.use(logger('dev'))
app.use(express.json({ limit: '2mb' }))

// 註冊路由
app.get('/', (req, res) => {
    res.status(200).json({ message: 'Hello world!' })
})

// catch 404 and forward to error handler
app.use((req, res, next) => {
    next(createError(404))
})

// error handler
app.use((err, req, res, next) => {
    // set locals, only providing error in development
    res.locals.message = err.message
    res.locals.error = config.debug ? err : {}

    // render the error page
    res.status(err.status || 500)
    res.send('error')
})

// 監聽電腦指定 port
app.listen(config.port, async () => {
    console.log(new Date().toISOString(), `伺服器啟動 ${config.url}`)
})
