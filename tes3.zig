const std = @import("std");
const net = std.net;
const http = std.http;
const mem = std.mem;
const heap = std.heap;

const MAIN_URL = "https://academic.ui.ac.id/main/Authentication/";
const LOGIN_URL = "https://academic.ui.ac.id/main/Authentication/Index";
const CHANGE_ROLE_URL = "https://academic.ui.ac.id/main/Authentication/ChangeRole";
const ISI_IRS_URL = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit";
const SAVE_IRS = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanSave";
const RINGKASAN_URL = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanSummary";

const USERNAME = "wahyu.ridho";
const PASSWORD = "2424angga4242";
const TERM = "Term 1";

var SAVED_TEXT: []u8 = undefined;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var client = http.Client{ .allocator = allocator };
    defer client.deinit();

    while (true) {
        std.debug.print("Try to login\n", .{});
        if (!try login(&client)) {
            std.debug.print("Login failed. Retrying...\n", .{});
            continue;
        }

        while (!try changeRole(&client)) {
            std.debug.print("Failed to change role. Retrying...\n", .{});
        }

        if (!mem.containsAtLeast(u8, SAVED_TEXT, 1, TERM)) {
            const now = std.time.timestamp();
            std.debug.print("War not started {}\n", .{now});
            continue;
        }

        var text: []u8 = undefined;
        while (true) {
            std.debug.print("Try to open isi siak page\n", .{});
            text = try getSiakPage(&client, allocator);
            if (text.len == 0) {
                std.debug.print("Failed to open isi siak page. Retrying...\n", .{});
                continue;
            }
            break;
        }

        const token_value = try extractToken(text, allocator);

        var payload = std.ArrayList(u8).init(allocator);
        defer payload.deinit();
        try payload.appendSlice("tokens=");
        try payload.appendSlice(token_value);
        try payload.appendSlice("&c[CSGE602012_01.00.12.01-2020]=724680-3");
        try payload.appendSlice("&c[CSGE602091_01.00.12.01-2020]=724707-3");
        try payload.appendSlice("&c[CSGE602022_01.00.12.01-2020]=724720-4");
        try payload.appendSlice("&c[CSGE602040_01.00.12.01-2020]=724748-4");
        try payload.appendSlice("&c[CSIM602155_01.00.12.01-2020]=725467-3");
        try payload.appendSlice("&comment=&submit=Simpan IRS");

        std.debug.print("Try to fill IRS\n", .{});
        while (true) {
            if (!try fillIRS(&client, payload.items)) {
                std.debug.print("Failed to fill IRS. Retrying...\n", .{});
                continue;
            }
            break;
        }

        _ = try getRingkasan(&client);
    }
}

fn login(client: *http.Client) !bool {
    var headers = http.Headers{ .allocator = client.allocator };
    defer headers.deinit();
    try headers.append("Content-Type", "application/x-www-form-urlencoded");

    var req = try client.request(.POST, try std.Uri.parse(LOGIN_URL), headers, .{});
    defer req.deinit();
    try req.start();
    try req.writeAll(std.fmt.allocPrint(client.allocator, "username={}&password={}", .{USERNAME, PASSWORD}));
    try req.finish();

    var response = try req.wait();
    const body = try response.reader().readAllAlloc(client.allocator, 1024 * 1024);
    defer client.allocator.free(body);

    if (!mem.containsAtLeast(u8, body, 1, "redirecting...")) {
        std.debug.print("Terjadi masalah saat melakukan Login ke Siak\n", .{});
        return false;
    }
    if (mem.containsAtLeast(u8, body, 1, "Login Failed")) {
        return false;
    }
    return true;



}

fn changeRole(client: *http.Client) !bool {
    var req = try client.request(.GET, try std.Uri.parse(CHANGE_ROLE_URL), .{}, .{});
    defer req.deinit();
    try req.start();
    try req.finish();

    var response = try req.wait();
    const body = try response.reader().readAllAlloc(client.allocator, 1024 * 1024);
    defer client.allocator.free(body);

    if (!mem.containsAtLeast(u8, body, 1, "WAHYU RIDHO") and !mem.containsAtLeast(u8, body, 1, "Mahasiswa")) {
        std.debug.print("Gagal dalam mengganti role\n", .{});
        return false;
    }
    SAVED_TEXT = body;
    return true;
}

fn getSiakPage(client: *http.Client, allocator: mem.Allocator) ![]u8 {
    var req = try client.request(.GET, try std.Uri.parse(ISI_IRS_URL), .{}, .{});
    defer req.deinit();
    try req.start();
    try req.finish();

    var response = try req.wait();
    const body = try response.reader().readAllAlloc(allocator, 1024 * 1024);

    if (!mem.containsAtLeast(u8, body, 1, "Pengisian IRS")) {
        std.debug.print("Gagal dalam membuka halaman Pengisian IRS\n", .{});
        return &[_]u8{};
    }
    return body;
}

fn fillIRS(client: *http.Client, payload: []const u8) !bool {
    var headers = http.Headers{ .allocator = client.allocator };
    defer headers.deinit();
    try headers.append("Content-Type", "application/x-www-form-urlencoded");

    var req = try client.request(.POST, try std.Uri.parse(SAVE_IRS), headers, .{});
    defer req.deinit();
    try req.start();
    try req.writeAll(payload);
    try req.finish();

    var response = try req.wait();
    const body = try response.reader().readAllAlloc(client.allocator, 1024 * 1024);
    defer client.allocator.free(body);

    if (mem.containsAtLeast(u8, body, 1, "IRS berhasil tersimpan!")) {
        std.debug.print("Berhasil tersimpan!\n", .{});
        return true;
    } else {
        std.debug.print("Gagal menyimpan IRS\n", .{});
        return false;
    }
}

fn getRingkasan(client: *http.Client) !bool {
    var req = try client.request(.GET, try std.Uri.parse(RINGKASAN_URL), .{}, .{});
    defer req.deinit();
    try req.start();
    try req.finish();

    var response = try req.wait();
    const body = try response.reader().readAllAlloc(client.allocator, 1024 * 1024);
    defer client.allocator.free(body);

    if (!mem.containsAtLeast(u8, body, 1, "Ringkasan")) {
        std.debug.print("Gagal membuka halaman Ringkasan Pengisian IRS\n", .{});
        return false;
    }
    std.debug.print("Berhasil\n", .{});
    return true;
}

fn extractToken(html: []const u8, allocator: mem.Allocator) ![]const u8 {
    var token_value: []const u8 = "";
    var it = mem.split(u8, html, "<input");
    while (it.next()) |input_tag| {
        if (mem.containsAtLeast(u8, input_tag, 1, "name=\"tokens\"")) {
            var value_it = mem.split(u8, input_tag, "value=\"");
            if (value_it.next()) |_| {
                if (value_it.next()) |value| {
                    const end = mem.indexOfScalar(u8, value, '"') orelse value.len;
                    token_value = try allocator.dupe(u8, value[0..end]);
                    break;
                }
            }
        }
    }
    return token_value;
}