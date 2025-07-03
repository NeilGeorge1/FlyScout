using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using FlyScout.Models;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Microsoft.AspNetCore.Authorization;

namespace FlyScout.Controllers;

[Authorize]
public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly IConfiguration _config;

    public HomeController(ILogger<HomeController> logger, IHttpClientFactory httpClientFactory, IConfiguration config)
    {
        _logger = logger;
        _httpClientFactory = httpClientFactory;
        _config = config;
    }

    public IActionResult Index()
    {
        return View();
    }

    [HttpPost]
    public IActionResult RunScripts(string from, string to, DateTime date)
    {
        string formattedDate = date.ToString("ddd MMM dd yyyy");
        List<string> paths = new List<string> { "Scrapers/goibibo.py"};

        List<string> allOutputs = new List<string>();

        foreach (string scriptPath in paths)
        {
            var psi = new ProcessStartInfo();
            psi.FileName = "/home/neil/Projects/FlyScout/Scrapers/env/bin/python";
            psi.Arguments = $"{scriptPath} \"{from}\" \"{to}\" \"{formattedDate}\"";
            psi.UseShellExecute = false;
            psi.RedirectStandardOutput = true;
            psi.CreateNoWindow = true;

            var process = Process.Start(psi);
            string output = process.StandardOutput.ReadToEnd();
            process.WaitForExit();

            allOutputs.Add(output);
        }

        TempData["ScriptOutput"] = string.Join("\n---\n", allOutputs);
        return RedirectToAction("Result");
    }

    public IActionResult Result()
    {
        var result = TempData["ScriptOutput"] as string ?? "No results available.";
        return View(model: result);
    }

    public IActionResult Privacy()
    {
        return View();
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }

    // 👇 Chatbot API endpoint
    [HttpPost]
    public async Task<IActionResult> Chat(string userInput)
    {
        if (string.IsNullOrWhiteSpace(userInput))
            return Json(new { error = "Input cannot be empty." });

        try
        {
            string response = await CallChatbotAPI(userInput);
            return Json(new { reply = response });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during chatbot interaction.");
            return Json(new { error = $"Error: {ex.Message}" });
        }
    }

    private async Task<string> CallChatbotAPI(string userInput)
    {
        using var client = _httpClientFactory.CreateClient();
            
        // Set headers
        client.DefaultRequestHeaders.Clear();
        var apiKey = _config["Cohere:ApiKey"];
        client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
        client.DefaultRequestHeaders.Add("accept", "application/json");
Console.WriteLine("ENV KEY: " + Environment.GetEnvironmentVariable("COHERE_API_KEY"));

        //in context learning
        var promptWithContext = @"
        You are a helpful, knowledgeable, and friendly flight assistant.

        User: What airlines fly from Mumbai to Bangalore?
        Bot: Some common airlines include IndiGo, Air India, and Akasa Air.

        User: How long is the flight from Delhi to Chennai?
        Bot: It usually takes about 2.5 hours.

        User: What is the baggage allowance in economy?
        Bot: Most airlines allow 15 kg for check-in and 7 kg for carry-on in economy class.

        User: Can I carry food onboard?
        Bot: Yes, you can usually carry food onboard, but liquids over 100ml are restricted.

        User: Whats the meal option in Business Class?
        Bot: Business Class usually offers multiple gourmet meal options, including vegetarian and non-vegetarian choices.

        User: " + userInput;

        // Prepare request payload
        var requestPayload = new
        {
            model = "command-r-plus",
            prompt = promptWithContext,
            max_tokens = 100,
            temperature = 0.3
        };

        var jsonPayload = JsonConvert.SerializeObject(requestPayload);
        Console.WriteLine($"Request payload: {jsonPayload}");

        var content = new StringContent(jsonPayload, System.Text.Encoding.UTF8, "application/json");
        
        var response = await client.PostAsync("https://api.cohere.ai/generate", content);
        var responseString = await response.Content.ReadAsStringAsync();
        
        Console.WriteLine($"API Response Status: {response.StatusCode}");
        Console.WriteLine($"API Response: {responseString}");

        if (!response.IsSuccessStatusCode)
        {
            throw new Exception($"API call failed: {response.StatusCode} - {response.ReasonPhrase}. Response: {responseString}");
        }

        // Parse response more safely
        try
        {
            var jsonResponse = JObject.Parse(responseString);
            
            // Log the structure for debugging
            Console.WriteLine($"Parsed JSON structure: {jsonResponse}");

            // Try different possible response formats
            if (jsonResponse["generations"] != null && jsonResponse["generations"].HasValues)
            {
                var firstGeneration = jsonResponse["generations"]?[0];
                if (firstGeneration?["text"] != null)
                {
                    return firstGeneration["text"]?.ToString()?.Trim() ?? "Empty response";
                }
            }
            
            // Alternative: check if response is directly in "text" field
            if (jsonResponse["text"] != null)
            {
                return jsonResponse["text"]?.ToString()?.Trim() ?? "Empty response";
            }

            // Alternative: check if it's in a "completion" field
            if (jsonResponse["completion"] != null)
            {
                return jsonResponse["completion"]?.ToString()?.Trim() ?? "Empty response";
            }

            // If none of the above work, return the entire response for debugging
            return $"Unexpected response format. Full response: {responseString}";
        }
        catch (JsonException ex)
        {
            Console.WriteLine($"JSON parsing error: {ex.Message}");
            return $"Error parsing API response: {ex.Message}. Raw response: {responseString}";
        }
    }

}
