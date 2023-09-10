using System.Net.Http.Headers;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// 讀取應用程式參數
string lineChannelAccessToken = builder.Configuration["LINE_CHANNEL_ACCESS_TOKEN"];
string lineChannelSecret = builder.Configuration["LINE_CHANNEL_SECRET"];
Console.WriteLine(lineChannelAccessToken);
Console.WriteLine(lineChannelSecret);

// 建立 HTTP Client
var httpClient = new HttpClient() {
    BaseAddress = new Uri("https://api.line.me/v2/"),
};
httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", lineChannelAccessToken);
httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment()) {
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.MapGet("/", () => "Hello world!");

app.Run();
