#!/bin/bash
# Please run `chmod +x run.sh` before executing the script
# to give it permission on your device

# Initial values
c=true
lo=true
s0=true

# Counter variable
test_count=1

# Loop through the 8 combinations of c, lo and s0 (2^3 = 8)
for ((i=1; i<=8; i++)); do

  c_var=""
  lo_var=""
  s0_var=""

 if [ $c == true ] && [ $lo == true ] && [ $s0 == true ]; then
      c_var="c=True"
      lo_var="lo=True"
      s0_var="s0=True"
      c=true
      lo=true
      s0=false
  elif [ $c == true ] && [ $lo == true ] && [ $s0 == false ]; then
      c_var="c=True"
      lo_var="lo=True"
      s0_var="s0=False"
      c=true
      lo=false
      s0=true
  elif [ $c == true ] && [ $lo == false ] && [ $s0 == true ]; then
      c_var="c=True"
      lo_var="lo=False"
      s0_var="s0=True"
      c=true
      lo=false
      s0=false
  elif [ $c == true ] && [ $lo == false ] && [ $s0 == false ]; then
      c_var="c=True"
      lo_var="lo=False"
      s0_var="s0=False"
      c=false
      lo=true
      s0=true
  elif [ $c == false ] && [ $lo == true ] && [ $s0 == true ]; then
      c_var="c=False"
      lo_var="lo=True"
      s0_var="s0=True"
      c=false
      lo=true
      s0=false
  elif [ $c == false ] && [ $lo == true ] && [ $s0 == false ]; then
      c_var="c=False"
      lo_var="lo=True"
      s0_var="s0=False"
      c=false
      lo=false
      s0=true
  elif [ $c == false ] && [ $lo == false ] && [ $s0 == true ]; then
      c_var="c=False"
      lo_var="lo=False"
      s0_var="s0=True"
      c=false
      lo=false
      s0=false
  elif [ $c == false ] && [ $lo == false ] && [ $s0 == false ]; then
      c_var="c=False"
      lo_var="lo=False"
      s0_var="s0=False"
      c=true
      lo=true
      s0=true
  fi

  # Run the make command with the appropriate flags
  make -C .. op=8 m=2 n=2 p=2 $c_var $lo_var $s0_var test=1 exp=1 tc="$test_count" -s
  ((test_count++))

  make -C .. op=7 m=2 n=2 p=2 $c_var $lo_var $s0_var test=1 exp=1 tc="$test_count" -s
  ((test_count++))

  make -C .. op=2 m=2 n=1 p=1 $c_var $lo_var $s0_var test=1 exp=1 tc="$test_count" -s
  ((test_count++))

  make -C .. op=2 m=1 n=2 p=1 $c_var $lo_var $s0_var test=1 exp=1 tc="$test_count" -s
  ((test_count++))

  make -C .. op=2 m=1 n=1 p=2 $c_var $lo_var $s0_var test=1 exp=1 tc="$test_count" -s
  ((test_count++))

  make -C .. op=6 m=3 n=2 p=1 $c_var $lo_var $s0_var test=1 exp=1 tc="$test_count" -s
  ((test_count++))

  make -C .. op=6 m=1 n=3 p=2 $c_var $lo_var $s0_var test=1 exp=1 tc="$test_count" -s
  ((test_count++))

  make -C .. op=6 m=1 n=2 p=3 $c_var $lo_var $s0_var test=1 exp=1 tc="$test_count" -s
  ((test_count++))

  make -C .. op=4 m=2 n=2 p=2 $c_var $lo_var $s0_var test=1 exp=0 tc="$test_count" -s
  ((test_count++))

  make -C .. op=3 m=4 n=4 p=1 $c_var $lo_var $s0_var test=1 exp=0 tc="$test_count" -s
  ((test_count++))

  make -C .. op=4 m=1 n=4 p=4 $c_var $lo_var $s0_var test=1 exp=0 tc="$test_count" -s
  ((test_count++))

  make -C .. op=3 m=4 n=1 p=4 $c_var $lo_var $s0_var test=1 exp=0 tc="$test_count" -s
  ((test_count++))

  make -C .. op=3 m=3 n=2 p=1 $c_var $lo_var $s0_var test=1 exp=0 tc="$test_count" -s
  ((test_count++))

  make -C .. op=4 m=1 n=3 p=2 $c_var $lo_var $s0_var test=1 exp=0 tc="$test_count" -s
  ((test_count++))

  make -C .. op=4 m=1 n=2 p=3 $c_var $lo_var $s0_var test=1 exp=0 tc="$test_count" -s
  ((test_count++))

done

# Check streamlining
make -C .. op=23 m=3 n=3 p=3 s1=True sp1=-1 test=1 exp=1 tc="$test_count" -s
((test_count++))

make -C .. op=23 m=3 n=3 p=3 s1=True sp1=600 test=1 exp=1 tc="$test_count" -s
((test_count++))

make -C .. op=7 m=2 n=2 p=2 s3=True sp3=1 test=1 exp=1 tc="$test_count" -s
