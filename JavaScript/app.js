import createError from 'http-errors'
import express from 'express'
import logger from 'morgan'

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
    res.locals.error = req.app.get('env') === 'development' ? err : {}

    // render the error page
    res.status(err.status || 500)
    res.json({ message: 'error' })
})

// 監聽電腦指定 port
app.listen(3000, async () => {
    console.log(new Date().toISOString(), '伺服器啟動')
})
