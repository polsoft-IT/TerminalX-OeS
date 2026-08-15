# archive - Archive Commands

## NAME

archive - Archive commands (zip, unzip, 7z, un7z, tar, untar, iso)

## DESCRIPTION

The archive command provides comprehensive archive management capabilities. Create, extract, and manage various archive formats including ZIP, 7z, TAR, and ISO with 26 available commands.

## SYNOPSIS

```
archive zip <files> <output>
archive unzip <archive> <dest>
archive 7z <files> <output>
archive un7z <archive> <dest>
archive tar <files> <output>
archive untar <archive> <dest>
archive iso create <dir> <output>
archive iso extract <iso> <dest>
archive iso mount <iso>
archive iso unmount
archive rar <files> <output>
archive unrar <archive> <dest>
archive gz <file>
archive gunzip <archive>
archive bz2 <file>
archive bunzip2 <archive>
archive xz <file>
archive unxz <archive>
archive list <archive>
archive info <archive>
archive test <archive>
archive verify <archive>
```

## OPTIONS

- `zip <files> <output>` - Create ZIP archive
- `unzip <archive> <dest>` - Extract ZIP archive
- `7z <files> <output>` - Create 7z archive
- `un7z <archive> <dest>` - Extract 7z archive
- `tar <files> <output>` - Create TAR archive
- `untar <archive> <dest>` - Extract TAR archive
- `iso create <dir> <output>` - Create ISO image
- `iso extract <iso> <dest>` - Extract ISO image
- `list <archive>` - List archive contents
- `info <archive>` - Show archive information

## EXAMPLES

```
archive zip *.txt backup.zip
archive unzip backup.zip /home/user/backup
archive tar project.tar.gz project/
archive iso extract image.iso /mnt/iso
```

## SEE ALSO

man(1), fs(1), compress(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
