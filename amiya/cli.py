"""
Command-line interface for AMIYA AI Assistant.
"""

import click
import logging
import json
import time
from typing import Optional
import sys

from amiya import AmiyaAssistant

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.option('--debug', is_flag=True, help='Enable debug logging')
@click.option('--model-path', help='Path to custom YOLO model')
@click.pass_context
def cli(ctx, debug, model_path):
    """AMIYA AI Assistant - Computer vision-based universal AI assistant."""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    ctx.ensure_object(dict)
    ctx.obj['model_path'] = model_path


@cli.command()
@click.option('--region', help='Capture region as "x,y,width,height"')
@click.option('--output', help='Save analysis to JSON file')
@click.pass_context
def analyze(ctx, region, output):
    """Analyze current screen for UI elements."""
    try:
        assistant = AmiyaAssistant(model_path=ctx.obj.get('model_path'))
        
        # Parse region if provided
        region_tuple = None
        if region:
            try:
                parts = [int(x.strip()) for x in region.split(',')]
                if len(parts) == 4:
                    region_tuple = tuple(parts)
                else:
                    click.echo("Error: Region must be 'x,y,width,height'", err=True)
                    return
            except ValueError:
                click.echo("Error: Invalid region format", err=True)
                return
        
        click.echo("Capturing and analyzing screen...")
        analysis = assistant.capture_and_analyze(region_tuple)
        
        if analysis:
            ui_count = len(analysis.get('ui_elements', []))
            text_count = len(analysis.get('text_regions', []))
            context = analysis.get('context', 'unknown')
            
            click.echo(f"Analysis complete:")
            click.echo(f"  - UI elements detected: {ui_count}")
            click.echo(f"  - Text regions detected: {text_count}")
            click.echo(f"  - Context: {context}")
            
            # Show suggestions
            suggestions = assistant.get_assistance_suggestions()
            if suggestions:
                click.echo("\nSuggested actions:")
                for i, suggestion in enumerate(suggestions, 1):
                    click.echo(f"  {i}. {suggestion}")
            
            # Save to file if requested
            if output:
                # Convert numpy arrays to lists for JSON serialization
                json_data = _prepare_for_json(analysis)
                with open(output, 'w') as f:
                    json.dump(json_data, f, indent=2)
                click.echo(f"\nAnalysis saved to {output}")
        else:
            click.echo("Error: Analysis failed", err=True)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument('task_description')
@click.pass_context
def assist(ctx, task_description):
    """Provide assistance with a specific task."""
    try:
        assistant = AmiyaAssistant(model_path=ctx.obj.get('model_path'))
        
        click.echo(f"Assisting with task: {task_description}")
        success = assistant.assist_with_task(task_description)
        
        if success:
            click.echo("Task assistance completed successfully")
        else:
            click.echo("Task assistance failed or no action taken", err=True)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument('x', type=int)
@click.argument('y', type=int)
@click.option('--button', default='left', help='Mouse button (left, right, middle)')
@click.option('--clicks', default=1, help='Number of clicks')
@click.pass_context
def click_at(ctx, x, y, button, clicks):
    """Click at specific coordinates."""
    try:
        assistant = AmiyaAssistant(model_path=ctx.obj.get('model_path'))
        
        click.echo(f"Clicking at ({x}, {y}) with {button} button, {clicks} times")
        success = assistant.interaction_controller.click(x, y, button, clicks)
        
        if success:
            click.echo("Click completed successfully")
        else:
            click.echo("Click failed", err=True)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument('text')
@click.option('--interval', default=0.05, help='Interval between keystrokes')
@click.pass_context
def type_text(ctx, text, interval):
    """Type text at current cursor position."""
    try:
        assistant = AmiyaAssistant(model_path=ctx.obj.get('model_path'))
        
        click.echo(f"Typing: {text[:50]}{'...' if len(text) > 50 else ''}")
        success = assistant.interaction_controller.type_text(text, interval)
        
        if success:
            click.echo("Text typed successfully")
        else:
            click.echo("Text typing failed", err=True)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument('element_type')
@click.option('--confidence', default=0.5, help='Minimum confidence threshold')
@click.pass_context
def find_and_click(ctx, element_type, confidence):
    """Find and click a UI element of specified type."""
    try:
        assistant = AmiyaAssistant(model_path=ctx.obj.get('model_path'))
        
        click.echo("Analyzing screen...")
        assistant.capture_and_analyze()
        
        click.echo(f"Looking for {element_type} with confidence >= {confidence}")
        element = assistant.find_element(element_type, confidence)
        
        if element:
            click.echo(f"Found {element_type} at {element.center} (confidence: {element.confidence:.2f})")
            success = assistant.click_element(element)
            
            if success:
                click.echo("Element clicked successfully")
            else:
                click.echo("Failed to click element", err=True)
        else:
            click.echo(f"No {element_type} found with sufficient confidence", err=True)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.option('--format', 'output_format', default='text', 
              type=click.Choice(['text', 'json']), help='Output format')
@click.pass_context
def status(ctx, output_format):
    """Show assistant status and capabilities."""
    try:
        assistant = AmiyaAssistant(model_path=ctx.obj.get('model_path'))
        status_info = assistant.get_status()
        
        if output_format == 'json':
            click.echo(json.dumps(status_info, indent=2))
        else:
            click.echo("AMIYA AI Assistant Status:")
            click.echo(f"  Initialized: {status_info['initialized']}")
            click.echo(f"  Safety Mode: {status_info['safety_mode']}")
            click.echo(f"  Current Context: {status_info['current_context']}")
            click.echo(f"  Detected Elements: {status_info['detected_elements_count']}")
            click.echo(f"  Screen Size: {status_info['screen_size']}")
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.pass_context
def demo(ctx):
    """Run a demonstration of AMIYA capabilities."""
    try:
        assistant = AmiyaAssistant(model_path=ctx.obj.get('model_path'))
        
        click.echo("AMIYA AI Assistant Demo")
        click.echo("======================")
        
        # Step 1: Analyze screen
        click.echo("\n1. Analyzing current screen...")
        analysis = assistant.capture_and_analyze()
        
        if analysis:
            ui_count = len(analysis.get('ui_elements', []))
            text_count = len(analysis.get('text_regions', []))
            context = analysis.get('context', 'unknown')
            
            click.echo(f"   - Found {ui_count} UI elements")
            click.echo(f"   - Found {text_count} text regions")
            click.echo(f"   - Context: {context}")
        
        # Step 2: Show suggestions
        click.echo("\n2. Getting assistance suggestions...")
        suggestions = assistant.get_assistance_suggestions()
        
        if suggestions:
            click.echo("   Available actions:")
            for i, suggestion in enumerate(suggestions, 1):
                click.echo(f"     {i}. {suggestion}")
        else:
            click.echo("   No suggestions available")
        
        # Step 3: Show mouse position
        click.echo("\n3. Current mouse position:")
        pos = assistant.interaction_controller.get_mouse_position()
        click.echo(f"   Mouse at: {pos}")
        
        click.echo("\nDemo completed! Try other commands for interactive assistance.")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


def _prepare_for_json(data):
    """Prepare data for JSON serialization by converting numpy arrays."""
    if isinstance(data, dict):
        return {k: _prepare_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_prepare_for_json(item) for item in data]
    elif hasattr(data, 'tolist'):  # numpy array
        return data.tolist()
    elif hasattr(data, '__dict__'):  # custom objects
        return {k: _prepare_for_json(v) for k, v in data.__dict__.items()}
    else:
        return data


def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()