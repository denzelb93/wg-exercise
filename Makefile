IMAGE			:= localhost/wg-file-api
CONTAINER		:= api-local
LOCAL_FILE_DIR  := $(shell cat src/config.json | jq .local_dir | sed -e 's/"//g')
API_FILE_DIR	:= /mnt/www/api/src/user_files

create-test-objects:
	- mkdir -p $(LOCAL_FILE_DIR)/testdir/subtestdir
	- echo "test 1st directory file 0" > $(LOCAL_FILE_DIR)/testdir/dirfile0.txt
	- echo "test second directory file 1" > $(LOCAL_FILE_DIR)/testdir/dirfile1.txt
	- echo "test a testfile" > $(LOCAL_FILE_DIR)/testfile.txt

build-local:
	- docker build . -t $(IMAGE)

run-local: build-local
	- mkdir -p $(LOCAL_FILE_DIR)
	- docker run -d -p 80:80 --name $(CONTAINER) -v $(LOCAL_FILE_DIR):$(API_FILE_DIR) $(IMAGE)

run-local-test: create-test-objects run-local
	- docker exec $(CONTAINER) bash src/tests/test.sh

stop-local:
	- docker stop $$(docker ps --format {{.Names}} | grep $(CONTAINER)) | true

clean:
	- make stop-local
	- docker rm -vf $$(docker ps -a -q --format {{.Names}}) | true
	- docker rmi -f $$(docker images -a -q | grep $(IMAGE)) | true
	- docker builder prune -f