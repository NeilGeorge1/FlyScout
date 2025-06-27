using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using FlyScout.Models;

namespace FlyScout.Controllers;

public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;

    public HomeController(ILogger<HomeController> logger)
    {
        _logger = logger;
    }

    public IActionResult Index()
    {
        return View(); // You should also have a Views/Home/Index.cshtml
    }

    [HttpPost]
    public IActionResult RunScripts(string from, string to, DateTime date)
    {
        string formattedDate = date.ToString("ddd MMM dd yyyy");
        List<string> paths = new List<string> { "Scrapers/goibibo.py", "Scrapers/make_my_trip.py"};

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
}
