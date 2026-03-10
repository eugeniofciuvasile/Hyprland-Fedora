srpm:
	dnf install -y rpm-build curl grep rpm-devtools
	./create-srpm.sh
	cp srpm/*.src.rpm $(outdir)
