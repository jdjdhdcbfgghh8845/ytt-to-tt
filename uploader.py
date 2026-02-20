from playwright.sync_api import sync_playwright
import os
import time

class TikTokUploader:
    def __init__(self, cookies_path="cookies.json"):
        self.cookies_path = cookies_path

    def upload_video(self, video_path, description, hashtags):
        if not os.path.exists(video_path):
            raise FileExistsError(f"Video file not found: {video_path}")

        full_description = f"{description}\n\n" + " ".join([f"#{h}" for h in hashtags])

        with sync_playwright() as p:
            app_data = os.environ['APPDATA']
            user_data_dir = os.path.join(app_data, 'Mozilla', 'Firefox', 'Profiles', '1p1wiuc7.default-release')
            browser = p.firefox.launch_persistent_context(user_data_dir, headless=False, no_viewport=True, args=['--allow-downgrade'])
            page = browser.new_page()

            page.goto("https://www.tiktok.com/upload?lang=en")
            
            # Check if we need to login
            if "login" in page.url.lower():
                print("Please log in manually in the opened browser...")
                # Wait for the user to login and reach the upload page
                page.wait_for_url("**/upload**", timeout=0)

            print("Starting upload process...")
            
            # TikTok Studio input is often hidden. We wait for it to be attached to DOM.
            page.wait_for_selector('input[type="file"]', state="attached", timeout=60000)
            page.set_input_files('input[type="file"]', video_path)

            print("Video uploaded. Filling metadata...")

            # Wait for processing and fill description
            # Caption field in TikTok Studio
            caption_selectors = [
                'div[contenteditable="true"]',
                '.notranslate.public-DraftEditor-content',
                '[data-contents="true"]'
            ]
            
            caption_filled = False
            for selector in caption_selectors:
                try:
                    page.wait_for_selector(selector, timeout=15000)
                    # Instead of fill, we use JavaScript to set the text and trigger input events
                    # This is more stable for TikTok's rich text editor
                    page.evaluate(f"""
                        (selector, text) => {{
                            const el = document.querySelector(selector);
                            el.innerText = text;
                            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                    """, selector, full_description)
                    print("Caption set successfully.")
                    caption_filled = True
                    break
                except Exception as e:
                    print(f"Selector {selector} failed: {str(e)}")
            
            if not caption_filled:
                print("Warning: Could not fill caption automatically.")

            # Wait for "Post" button
            try:
                print("Waiting for TikTok checks to complete and Post button to be ready...")
                
                post_found = False
                # We'll poll for the button for up to 2 minutes (checks can be slow)
                for attempt in range(24): # 24 * 5 seconds = 2 minutes
                    # Try multiple selectors for the Post button
                    selectors = [
                        'button:has-text("Post")',
                        '[data-e2e="ad-post-button"]'
                    ]
                    
                    for selector in selectors:
                        btn = page.locator(selector).first
                        if btn.is_visible() and btn.is_enabled():
                            print(f"Post button is ready! Clicking... (Attempt {attempt+1})")
                            btn.scroll_into_view_if_needed()
                            btn.click()
                            post_found = True
                            break
                    
                    if post_found:
                        break
                    
                    print(f"Still waiting for checks/button... {attempt * 5}s")
                    time.sleep(5)
                
                if not post_found:
                    print("Warning: Could not find or click an ENABLED Post button within 2 minutes.")
                else:
                    print("Post clicked! Waiting 20 seconds to ensure upload is finalized...")
                    time.sleep(20) # Keep browser open to finish the request

            except Exception as e:
                print(f"Error during final post: {str(e)}")
            
            browser.close()
            return True

if __name__ == "__main__":
    # Test uploader if a video exists
    # uploader = TikTokUploader()
    # uploader.upload_video("path_to_video.mp4", "Test upload", ["shorts", "test"])
    pass
