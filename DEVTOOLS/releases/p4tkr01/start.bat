@echo off

for /l %%i in (1, 1, 12) do (
  if not exist mh%%i (
    mkdir mh%%i
  )
  copy p4tk.py mh%%i
  copy stream.wpl mh%%i
  start cmd /c "cd mh%%i & python p4tk.py PATH"
)

echo Done!
pause