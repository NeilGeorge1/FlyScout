using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using FlyScout.Data;

var builder = WebApplication.CreateBuilder(args);

// Listen only on HTTP
builder.WebHost.UseUrls("http://localhost:5000");

// DB context
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));

// Identity
builder.Services.AddDefaultIdentity<IdentityUser>(options =>
{
    options.SignIn.RequireConfirmedAccount = false;
})
.AddEntityFrameworkStores<ApplicationDbContext>();

//chatbot
builder.Services.AddHttpClient();
builder.Services.AddSingleton<IConfiguration>(builder.Configuration);

// MVC
builder.Services.AddControllersWithViews(); // ✅ for MVC

var app = builder.Build();

// Disable HTTPS redirection
// app.UseHttpsRedirection();

app.UseStaticFiles();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();

// ✅ Map controller routes
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.MapRazorPages();

app.Run();
