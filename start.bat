@echo off

python texmover.py

for /l %%i in (1, 1, 12) do (
  if not exist mh%%i (
    mkdir mh%%i
  )
  copy p4tk.py mh%%i
  copy stream.wpl mh%%i
  start cmd /c "cd mh%%i & python p4tk.py PATH"

  if not exist nj1 (
    mkdir nj1
  )
  copy p4tk.py nj1
  copy stream.wpl nj1
  start cmd /c "cd nj1 & python p4tk.py PATH"

  if not exist nj2 (
    mkdir nj2
  )
  copy p4tk.py nj2
  copy stream.wpl nj2
  start cmd /c "cd nj2 & python p4tk.py PATH"

  if not exist nj3 (
    mkdir nj3
  )
  copy p4tk.py nj3
  copy stream.wpl nj3
  start cmd /c "cd nj3 & python p4tk.py PATH"

  if not exist nj4e (
    mkdir nj4e
  )
  copy p4tk.py nj4e
  copy stream.wpl nj4e
  start cmd /c "cd nj4e & python p4tk.py PATH"

  if not exist nj4w (
    mkdir nj4w
  )
  copy p4tk.py nj4w
  copy stream.wpl nj4w
  start cmd /c "cd nj4w & python p4tk.py PATH"

  if not exist nj5 (
    mkdir nj5
  )
  copy p4tk.py nj5
  copy stream.wpl nj5
  start cmd /c "cd nj5 & python p4tk.py PATH"

  if not exist njxr (
    mkdir njxr
  )
  copy p4tk.py njxr
  copy stream.wpl njxr
  start cmd /c "cd njxr & python p4tk.py PATH"

  if not exist njdocks (
    mkdir njdocks
  )
  copy p4tk.py njdocks
  copy stream.wpl njdocks
  start cmd /c "cd njdocks & python p4tk.py PATH"

  if not exist bronxe (
    mkdir bronxe
  )
  copy p4tk.py bronxe
  copy stream.wpl bronxe
  start cmd /c "cd bronxe & python p4tk.py PATH"

  if not exist bronxe2 (
    mkdir bronxe2
  )
  copy p4tk.py bronxe2
  copy stream.wpl bronxe2
  start cmd /c "cd bronxe2 & python p4tk.py PATH"

  if not exist bronxw (
    mkdir bronxw
  )
  copy p4tk.py bronxw