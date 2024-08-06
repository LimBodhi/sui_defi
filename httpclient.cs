using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Collections.Generic;
using HtmlAgilityPack;
using System.Net;

class Program
{
    private const string MAIN_URL = "https://academic.ui.ac.id/main/Authentication/";
    private const string LOGIN_URL = "https://academic.ui.ac.id/main/Authentication/Index";
    private const string CHANGE_ROLE_URL = "https://academic.ui.ac.id/main/Authentication/ChangeRole";
    private const string ISI_IRS_URL = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit";
    private const string SAVE_IRS = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanSave";
    private const string RINGKASAN_URL = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanSummary";

    private const string USERNAME = "";
    private const string PASSWORD = "";
    private const string TERM = "Term 1";

    private static string SAVEDTEXT = "";

    static async Task Main(string[] args)
    {
        while (true)
        {
            using (var handler = new HttpClientHandler())
            {
                handler.ServerCertificateCustomValidationCallback = (sender, cert, chain, sslPolicyErrors) => true;
                using (var client = new HttpClient(handler))
                {
                    try
                    {
                        Console.WriteLine("Try to login");
                        if (!await Login(client))
                        {
                            Console.WriteLine("Login failed. Retrying...");
                            continue;
                        }

                        while (!await ChangeRole(client))
                        {
                            Console.WriteLine("Failed to change role. Retrying...");
                        }

                        if (!SAVEDTEXT.Contains(TERM))
                        {
                            Console.WriteLine($"War not started {DateTime.Now}");
                            continue;
                        }

                        string text;
                        while (true)
                        {
                            Console.WriteLine("Try to open isi siak page");
                            text = await GetSiakPage(client);
                            if (string.IsNullOrEmpty(text))
                            {
                                Console.WriteLine("Failed to open isi siak page. Retrying...");
                                continue;
                            }
                            break;
                        }

                        var doc = new HtmlDocument();
                        doc.LoadHtml(text);
                        var tokenValue = doc.DocumentNode.SelectSingleNode("//input[@name='tokens']").GetAttributeValue("value", "");

                        var payload = new Dictionary<string, string>
                        {
                            { "tokens", tokenValue },
                            { "c[CSGE602012_01.00.12.01-2020]", "724680-3" },
                            { "c[CSGE602091_01.00.12.01-2020]", "724707-3" },
                            { "c[CSGE602022_01.00.12.01-2020]", "724720-4" },
                            { "c[CSGE602040_01.00.12.01-2020]", "724748-4" },
                            { "c[CSIM602155_01.00.12.01-2020]", "725467-3" },
                            { "comment", "" },
                            { "submit", "Simpan IRS" }
                        };

                        Console.WriteLine("Try to fill IRS");
                        while (true)
                        {
                            if (!await FillIRS(client, payload))
                            {
                                Console.WriteLine("Failed to fill IRS. Retrying...");
                                continue;
                            }
                            break;
                        }

                        await GetRingkasan(client);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine($"Error: {e.Message}");
                        continue;
                    }
                }
            }
        }
    }

    private static async Task<bool> Login(HttpClient client)
    {
        var content = new FormUrlEncodedContent(new[]
        {
            new KeyValuePair<string, string>("u", USERNAME),
            new KeyValuePair<string, string>("p", PASSWORD)
        });

        var response = await client.PostAsync(LOGIN_URL, content);
        var text = await response.Content.ReadAsStringAsync();

        if (!text.Contains("redirecting..."))
        {
            Console.WriteLine("Terjadi masalah saat melakukan Login ke Siak");
            return false;
        }
        if (text.Contains("Login Failed"))
        {
            return false;
        }
        return true;
    }

    private static async Task<bool> ChangeRole(HttpClient client)
    {
        var response = await client.GetAsync(CHANGE_ROLE_URL);
        var text = await response.Content.ReadAsStringAsync();

        if (!text.Contains("WAHYU RIDHO") && !text.Contains("Mahasiswa"))
        {
            Console.WriteLine("Gagal dalam mengganti role");
            return false;
        }
        SAVEDTEXT = text;
        return true;
    }

    private static async Task<string> GetSiakPage(HttpClient client)
    {
        var response = await client.GetAsync(ISI_IRS_URL);
        var text = await response.Content.ReadAsStringAsync();

        if (!text.Contains("Pengisian IRS"))
        {
            Console.WriteLine("Gagal dalam membuka halaman Pengisian IRS");
            return null;
        }
        return text;
    }

    private static async Task<bool> FillIRS(HttpClient client, Dictionary<string, string> payload)
    {
        var content = new FormUrlEncodedContent(payload);
        var response = await client.PostAsync(SAVE_IRS, content);
        var text = await response.Content.ReadAsStringAsync();

        if (text.Contains("IRS berhasil tersimpan!"))
        {
            Console.WriteLine("Berhasil tersimpan!");
            return true;
        }
        else
        {
            Console.WriteLine("Gagal menyimpan IRS");
            return false;
        }
    }

    private static async Task<bool> GetRingkasan(HttpClient client)
    {
        var response = await client.GetAsync(RINGKASAN_URL);
        var text = await response.Content.ReadAsStringAsync();

        if (!text.Contains("Ringkasan"))
        {
            Console.WriteLine("Gagal membuka halaman Ringkasan Pengisian IRS");
            return false;
        }
        Console.WriteLine("Berhasil");
        return true;
    }
}
