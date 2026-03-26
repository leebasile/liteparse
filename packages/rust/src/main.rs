use clap::{Parser, Subcommand, Args};
use liteparse_rs::extract;


#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

// 2. Define the top-level commands as an Enum.
#[derive(Subcommand, Debug)]
enum Commands {
    /// Extract text and metadata from a PDF file
    Extract(ExtractCommand),
}


#[derive(Args, Debug)]
struct ExtractCommand {
    /// Specify the path to the PDF file
    #[arg(long)]
    pdf_path: String,

    /// Optionally specify a target page number
    #[arg(long)]
    page_num: Option<u32>,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Extract(cmd) => {
            extract::extract(&cmd.pdf_path, cmd.page_num)?;
        }
    }

    Ok(())
}