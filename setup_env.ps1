# Check if Conda is available
if (!(Get-Command "conda" -ErrorAction SilentlyContinue)) {
    Write-Error "Conda is not installed or not in your PATH."
    exit 1
}

# Activate the environment
Write-Host "Activating environment 'yj_env'..."
conda activate yj_env

# Install Ruby from conda-forge
Write-Host "Installing Ruby..."
conda install -y -c conda-forge ruby

# Install Bundler
Write-Host "Installing Bundler..."
gem install bundler

# Install dependencies from Gemfile
Write-Host "Installing project dependencies..."
bundle install

Write-Host "Environment setup complete!"
