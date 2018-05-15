$srcdir = "C:\Users\mathir\Google Drive\bgs";
$destdir = "C:\bgs\";
$files = (Get-ChildItem $SrcDir -filter *.* | where-object {-not ($_.PSIsContainer)});
$files | foreach($_){
    if (!([system.io.file]::Exists($destdir+$_.name))) {
        cp $_.Fullname ($destdir+$_.name)
    };
}