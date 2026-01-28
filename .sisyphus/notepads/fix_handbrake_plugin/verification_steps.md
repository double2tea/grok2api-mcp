# User Verification Steps

## Prerequisites
- ✅ HandBrakeCLI installed and available at `/opt/homebrew/bin/HandBrakeCLI`
- ✅ DaVinci Resolve installed
- ✅ Plugin files deployed to `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins/com.sisyphus.handbrake.autoencode/`

## Step-by-Step Verification

### 1. Launch DaVinci Resolve
- Open DaVinci Resolve application
- Wait for it to fully load

### 2. Open Plugin
- Go to menu: **Workspace → Workflow Integrations**
- Look for "HandBrake Auto-Encode" in the list
- Click to open the plugin window

### 3. Expected Plugin Window
You should see:
- Dark-themed UI with status log
- Settings controls:
  - Quality slider (18-28)
  - Encoder dropdown (x264/x265)
  - Output Path text input
  - Auto-Open Folder checkbox
- "Save Settings" button
- "Test HandBrake" button
- Status log area showing "Plugin loaded successfully"

### 4. Test HandBrake Detection
- Click "Test HandBrake" button
- Status log should show:
  - ✅ "HandBrakeCLI found at: /opt/homebrew/bin/HandBrakeCLI"
  - ✅ HandBrake version info

### 5. Configure Settings
- Set Quality (e.g., 22)
- Choose Encoder (e.g., x264)
- Optionally set custom Output Path
- Enable Auto-Open Folder if desired
- Click "Save Settings"
- Status log should show: "Settings saved successfully"

### 6. Test Auto-Encode
- Open or create a project in Resolve
- Add a clip to timeline
- Go to Deliver page
- Set render settings and output path
- Click "Add to Render Queue"
- Click "Render All"
- Wait for render to complete

### 7. Expected Behavior
When render completes:
- Plugin status log should show: "Render job completed: [path]"
- HandBrakeCLI should automatically start encoding
- Progress updates should appear in status log
- When encoding completes: "HandBrake encoding completed successfully"
- Output folder should open (if Auto-Open enabled)
- Encoded file should exist: `[filename]_encoded.mp4`

## Troubleshooting

### Plugin doesn't appear in Workflow Integrations
- Check plugin directory exists: `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Workflow Integration Plugins/com.sisyphus.handbrake.autoencode/`
- Verify all files exist (manifest.xml, main.js, preload.js, renderer.js, index.html, config.json, WorkflowIntegration.node)
- Restart DaVinci Resolve

### Plugin window is blank
- Open DevTools (should auto-open)
- Check console for errors
- Verify WorkflowIntegration.node is correct architecture for your Mac

### Render not detected
- Check status log for errors
- Verify render actually completed in Resolve
- Try rendering again
- Plugin polls every 2 seconds, so there may be a slight delay

### HandBrake not found
- Run `which HandBrakeCLI` in terminal
- If not found, install HandBrake: `brew install handbrake`
- Restart plugin

### Encoding fails
- Check status log for error message
- Verify input file exists
- Verify output directory is writable
- Try manually running HandBrakeCLI to test
