import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class YoutubeDownloader {

    // UPDATE THIS: Change the path to your desired save location
    private static final String OUTPUT_PATH = "E:\\New folder";

    public static void main(String[] args) {
        // Ensure the folder exists before starting
        ensureDirectoryExists(OUTPUT_PATH);
        
        // Step 1: Update the backend engine (yt-dlp)
        updateYtDlp();

        Scanner scanner = new Scanner(System.in);
        
        try {
            System.out.print("\nEnter the URL of the audio/video: ");
            String url = scanner.nextLine().trim();
            if (url.isEmpty()) {
                System.out.println("[!] URL cannot be empty.");
                return;
            }

            System.out.print("Do you want to download (1) Audio or (2) Video? ");
            String choice = scanner.nextLine().trim();

            if (choice.equals("1")) {
                handleAudioDownload(scanner, url);
            } else if (choice.equals("2")) {
                handleVideoDownload(scanner, url);
            } else {
                System.out.println("[!] Invalid choice. Please enter 1 or 2.");
            }
        } catch (Exception e) {
            System.err.println("[!] An unexpected error occurred: " + e.getMessage());
        } finally {
            scanner.close();
        }
    }

    /**
     * Updates yt-dlp to the latest version to ensure compatibility with YouTube changes.
     */
    private static void updateYtDlp() {
        System.out.println("[*] Checking for yt-dlp updates and repairing dependencies...");
        runCommand("yt-dlp", "-U");
        System.out.println("[+] yt-dlp update check completed.");
    }

    private static void handleAudioDownload(Scanner scanner, String url) {
        System.out.print("Choose quality (128k or 256k): ");
        String quality = scanner.nextLine().trim().toLowerCase();

        if (quality.equals("128k") || quality.equals("256k")) {
            downloadAudio(url, quality);
        } else {
            System.out.println("[!] Invalid quality. Use 128k or 256k.");
        }
    }

    private static void handleVideoDownload(Scanner scanner, String url) {
        System.out.println("Available resolutions: 360p, 480p, 720p, 1080p, 1440p, 2160p, 4320p, 8640p, 15360p");
        System.out.print("Choose resolution: ");
        String res = scanner.nextLine().trim().toLowerCase();

        List<String> validRes = Arrays.asList(
            "360p", "480p", "720p", "1080p", "1440p", "2160p", "4320p", "8640p", "15360p"
        );

        if (validRes.contains(res)) {
            downloadVideo(url, res);
        } else {
            System.out.println("[!] Invalid resolution selected.");
        }
    }

    private static void downloadAudio(String url, String quality) {
        // Logic for audio format selection
        String format = quality.equals("128k") ? "bestaudio[abr<=128k]" : "bestaudio/best";
        String outPattern = OUTPUT_PATH + File.separator + "%(title)s.%(ext)s";
        
        System.out.println("[*] Extracting audio (" + quality + ")...");
        runCommand("yt-dlp", 
            "-x", 
            "--audio-format", "mp3", 
            "--audio-quality", quality.replace("k", ""), 
            "-f", format, 
            "-o", outPattern, 
            url
        );
        System.out.println("[+] Audio download and conversion complete.");
    }

    private static void downloadVideo(String url, String res) {
        // Logic for video resolution selection
        String height = res.replace("p", "");
        String format = "bestvideo[height<=" + height + "]+bestaudio/best[height<=" + height + "]";
        String outPattern = OUTPUT_PATH + File.separator + "%(title)s.%(ext)s";

        System.out.println("[*] Downloading video at " + res + "...");
        // Using MKV for high resolutions to ensure FFmpeg can merge high-end codecs
        runCommand("yt-dlp", 
            "-f", format, 
            "--merge-output-format", "mkv", 
            "-o", outPattern, 
            url
        );
        System.out.println("[+] Video download complete.");
    }

    /**
     * Executes external system commands and redirects output to the Java console.
     */
    private static void runCommand(String... args) {
        try {
            ProcessBuilder pb = new ProcessBuilder(args);
            pb.inheritIO(); // Shows progress bars and yt-dlp logs in your terminal
            Process process = pb.start();
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                System.err.println("[!] Process finished with error code: " + exitCode);
            }
        } catch (IOException | InterruptedException e) {
            System.err.println("[!] System command failed: " + e.getMessage());
        }
    }

    private static void ensureDirectoryExists(String path) {
        File dir = new File(path);
        if (!dir.exists()) {
            if (dir.mkdirs()) {
                System.out.println("[*] Created directory: " + path);
            }
        }
    }
}