# 🧩 StegoLab - Image Steganography Web Application

A modern, interactive web application for hiding and revealing secret messages in images using multiple steganographic techniques. Compare different methods with visual metrics and performance analysis.

## ✨ Features

- **Multiple Steganography Methods**: 
  - LSB (Least Significant Bit)
  - Palette-based
  - DCT (Discrete Cosine Transform)
  - XOR-based encoding
  
- **Dual Operation Modes**:
  - **Manual Mode**: Encode/decode with specific method selection
  - **Auto Compare Mode**: Test all methods simultaneously with comprehensive comparison

- **Visual Metrics & Analysis**:
  - SSIM (Structural Similarity Index)
  - PSNR (Peak Signal-to-Noise Ratio)
  - Encoding/Decoding time measurements
  - Interactive radar charts and performance graphs

- **Modern UI/UX**:
  - Responsive Bootstrap 5 design
  - Playful, cartoon-inspired interface
  - Real-time form interactions
  - Animated visualizations with Plotly

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd webapp
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to `http://localhost:5000`

### Dependencies

The application requires the following Python packages:

- **Flask** (>=2.3) - Web framework
- **Werkzeug** (>=2.3) - WSGI utilities
- **numpy** - Numerical computations
- **pillow** - Image processing
- **matplotlib** - Plotting and visualization
- **seaborn** - Statistical data visualization
- **pandas** - Data manipulation
- **opencv-python** - Computer vision
- **scikit-image** - Image processing algorithms
- **nbconvert**, **nbformat** - Jupyter notebook utilities

## 📁 Project Structure

```
webapp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/               # Static assets
│   ├── css/
│   │   └── styles.css    # Custom styling
│   └── js/
│       └── app.js        # Frontend interactions
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── manual.html       # Manual encode/decode mode
│   └── auto.html         # Auto comparison mode
├── uploads/              # Temporary upload storage
├── outputs/              # Generated stego images
└── outputs/plots/        # Performance comparison plots
```

## 🎯 Usage Guide

### Manual Mode

1. Navigate to **Encode/Decode** from the homepage
2. Upload an image file (PNG, JPG, JPEG, BMP, GIF)
3. Select operation mode:
   - **Encode**: Hide a secret message in the image
   - **Decode**: Extract a hidden message from a stego image
4. Choose a steganography method
5. For encoding:
   - Enter your secret message
   - Optionally specify output filename
6. Click **Run** to process

### Auto Compare Mode

1. Navigate to **Compare Methods** from the homepage
2. Upload an image and enter a secret message
3. Click **Run Comparison** to test all methods
4. View comprehensive results:
   - Side-by-side stego images
   - Performance metrics table
   - Interactive radar chart
   - SSIM/PSNR comparison graphs
   - Encoding/decoding time analysis

## 🧮 Supported Steganography Methods

| Method | Description | Best For |
|--------|-------------|----------|
| **LSB** | Least Significant Bit encoding | Simple text messages |
| **Palette** | Color palette manipulation | Images with limited colors |
| **DCT** | Discrete Cosine Transform | JPEG compression resilience |
| **XOR** | XOR-based pixel manipulation | Fast encoding/decoding |

## 📊 Metrics Explained

- **SSIM** (0-1): Higher values indicate better structural similarity
- **PSNR** (dB): Higher values indicate better quality (∞ for identical images)
- **Encode/Decode Time**: Performance measurement in seconds

## 🛠️ Configuration

### Environment Variables

- `FLASK_SECRET`: Secret key for session management (defaults to "dev-secret-key")
- `PORT`: Server port (defaults to 5000)

### File Uploads

- **Supported formats**: PNG, JPG, JPEG, BMP, GIF
- **Max file size**: Determined by Flask configuration
- **Storage**: Temporary files in `uploads/` directory
- **Cleanup**: Manual cleanup required for production use

## 🔧 Development

### Running in Development Mode

```bash
python app.py
```

The application runs with debug mode enabled by default.

### Custom Styling

The UI uses a playful theme with:
- Custom CSS variables in `static/css/styles.css`
- Bootstrap 5 framework
- Google Fonts (Nunito, Fredoka)
- Animated background blobs
- Hover effects and transitions

### Adding New Steganography Methods

1. Implement encode/decode functions in the backend project
2. Import functions in `app.py`
3. Add to `method_map()` dictionary
4. Update frontend if needed

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: Ensure parent project directory is in Python path
2. **File Upload Issues**: Check file permissions and supported formats
3. **Memory Issues**: Large images may require additional memory
4. **Plot Generation**: Ensure matplotlib backend is set to "Agg"

### Debug Mode

The application runs in debug mode by default. Disable for production:

```python
app.run(host="0.0.0.0", port=port, debug=False)
```

## 📝 License

This project is part of an academic steganography study. Please refer to the project's main license file.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request


---

**StegoLab** - Making steganography accessible and fun! 🎨🔐
