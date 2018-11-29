# deoplete-hack

[deoplete](https://github.com/Shougo/deoplete.nvim) source for 
[Hack](http://hacklang.org/).

## Install

You need to have [Hack 
setup](https://docs.hhvm.com/hack/getting-started/getting-started) before you 
can use it inside Vim.

Use your favorite plugin manager and add `yichenshen/deoplete-hack` to your `.vimrc`:

    Plug 'yichenshen/deoplete-hack'
    # or
    Plugin 'yichenshen/deoplete-hack'
    # or
    NeoBundle 'yichenshen/deoplete-hack'

## Options

* `g:deoplete#sources#hack#hh_client` (default `'hh_client'`): path to 
  `hh_client`.
* `g:deoplete#sources#hack#timeout` (default `0.5`): timeout (in seconds) for 
  `hh_client` response.
* `g:deoplete#sources#hack#debug` (default `0`): debug mode, errors in the  
  script will be surfaced in vim if this is `1`
