set nocompatible
set backspace=indent,eol,start
set expandtab
set ts=4
set ignorecase
set smartcase
set autoindent
set hlsearch
set incsearch
syntax on

if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

nnoremap <C-n> :next<CR>
nnoremap <C-p> :prev<CR>

" clear search highlights
" :let @/ = ""
" pastes random letters:
" nnoremap <esc><esc> :noh<return>

" has a delay:
" nnoremap <esc> :noh<enter><esc>
