"""
Check which dependencies are installed and which are missing
"""

import sys

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True, "✓ Installed"
    except ImportError:
        return False, "✗ Missing"

print("=" * 60)
print("Checking Python Dependencies")
print("=" * 60)
print()

# Core packages (required)
print("CORE PACKAGES (Required):")
packages = [
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn"),
    ("yfinance", "yfinance"),
    ("pandas", "pandas"),
    ("numpy", "numpy"),
    ("pydantic", "pydantic"),
    ("schedule", "schedule"),
]

core_installed = 0
for pkg_name, import_name in packages:
    installed, status = check_package(pkg_name, import_name)
    print(f"  {status} {pkg_name}")
    if installed:
        core_installed += 1

print()

# Optional packages (for AI features)
print("OPTIONAL PACKAGES (For AI Predictions):")
optional_packages = [
    ("tensorflow", "tensorflow"),
    ("scikit-learn", "sklearn"),
    ("google-generativeai", "google.generativeai"),
]

optional_installed = 0
for pkg_name, import_name in optional_packages:
    installed, status = check_package(pkg_name, import_name)
    print(f"  {status} {pkg_name}")
    if installed:
        optional_installed += 1

print()
print("=" * 60)
print("SUMMARY:")
print("=" * 60)

if core_installed == len(packages):
    print("✓ All core packages installed!")
    print("  You can run: python main_minimal.py")
    print()
else:
    print(f"✗ Missing {len(packages) - core_installed} core package(s)")
    print("  Run: install_minimal.bat")
    print()

if optional_installed == len(optional_packages):
    print("✓ All optional packages installed!")
    print("  You can run: python main.py (full version)")
    print()
else:
    print(f"⚠ Missing {len(optional_packages) - optional_installed} optional package(s)")
    print("  AI predictions will be disabled")
    print("  To enable: pip install tensorflow google-generativeai scikit-learn")
    print()

print("=" * 60)
print()

# Recommendations
if core_installed == len(packages) and optional_installed < len(optional_packages):
    print("RECOMMENDATION:")
    print("  Start with the minimal version:")
    print("    python main_minimal.py")
    print()
    print("  Install AI packages later when you have time:")
    print("    pip install tensorflow google-generativeai scikit-learn --timeout 600")
    print()
elif core_installed < len(packages):
    print("NEXT STEPS:")
    print("  1. Run: install_minimal.bat")
    print("  2. Then run: python main_minimal.py")
    print()
else:
    print("READY TO GO:")
    print("  Run: python main.py")
    print()

input("Press Enter to exit...")
