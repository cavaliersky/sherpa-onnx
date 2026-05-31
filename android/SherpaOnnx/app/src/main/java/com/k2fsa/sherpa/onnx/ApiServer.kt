import fi.iki.elonen.NanoHTTPD
import java.io.File

class ApiServer(port: Int, val recognizer: OfflineRecognizer) : NanoHTTPD(port) {
    override fun serve(session: IHTTPSession): Response {
        if (session.uri == "/recognize" && session.method == Method.POST) {
            val files = HashMap<String, String>()
            session.parseBody(files)
            
            // 获取上传的 wav 文件路径
            val wavPath = files["file"] ?: return newFixedLengthResponse("Error")
            
            // 调用 NPU 识别
            val text = recognizer.decode(wavPath)
            
            return newFixedLengthResponse("""{"status":"success", "text":"$text"}""")
        }
        return newFixedLengthResponse("API is running on NPU!")
    }
}
