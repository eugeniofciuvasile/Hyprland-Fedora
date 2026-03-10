srpm:
	dnf install -y rpmdevtools || dnf install -y rpm-build
	chmod +x create-srpm.sh
	./create-srpm.sh
	cp srpm/*.src.rpm $(outdir)
