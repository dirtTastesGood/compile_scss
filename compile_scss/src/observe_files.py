import time
from click import echo
from os import system 
from src.utilities import get_raw_scss, write_css, get_include_paths
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from sass import CompileError

def create_observer(config):
    '''
    Create a Watchdog Observer instance to watch SCSS directory 
    specified in the config.
    '''

    patterns = '*'
    ignore_patterns = ''
    ignore_directories = ''
    
    fileChangeHandler = PatternMatchingEventHandler(
        patterns = patterns,  # watched patterns
        ignore_patterns = ignore_patterns,  # ignored patterns
        ignore_directories = ignore_directories,  # ignored directories
        case_sensitive = True
    )

    def on_change(event, config=config):
        '''
        Executed on every change within the SCSS directory
        '''
        scss_dir = config['scss_dir']
        file_tree = get_include_paths(scss_dir)
        raw_scss = get_raw_scss(file_tree, scss_dir)
        write_css(raw_scss, config)

        echo(f"\nWatching {config['scss_dir']}...")
        echo("Press Ctrl + C to stop.")


    fileChangeHandler.on_modified = on_change
    fileChangeHandler.on_created  = on_change
    fileChangeHandler.on_moved    = on_change
    fileChangeHandler.on_deleted  = on_change

    path = config['scss_dir']
    observer = Observer()
    observer.schedule(
        fileChangeHandler,
        path,
        recursive=True
    )

    return observer

