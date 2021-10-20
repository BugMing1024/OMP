import { Input, Button, Pagination, Empty, Spin } from "antd";
import { useEffect, useState } from "react";
import styles from "./index.module.less";
import { SearchOutlined, DownloadOutlined } from "@ant-design/icons";
import Card from "./config/card.js";
import { useSelector } from "react-redux";
import { useHistory } from "react-router-dom";
import { fetchGet } from "@/utils/request";
import { apiRequest } from "@/config/requestApi";
import { handleResponse } from "@/utils/utils";

const AppStore = () => {
  // 视口高度
  const viewHeight = useSelector((state) => state.layouts.viewSize.height);
  const history = useHistory();
  const [tabKey, setTabKey] = useState("component");
  const [searchKey, setSearchKey] = useState("全部");
  const [searchData, setSearchData] = useState([]);

  const [searchName, setSearchName] = useState("");

  const [total, setTotal] = useState(0)

  const [loading, setLoading] = useState(false);
  const [dataSource, setDataSource] = useState([]);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: viewHeight > 955 ? 12 : 8,
    total: 0,
    searchParams: {},
  });

  function fetchData(pageParams = { current: 1, pageSize: 8 }, searchParams) {
    setLoading(true);
    fetchGet(
      searchParams.tabKey == "component"
        ? apiRequest.appStore.queryComponents
        : apiRequest.appStore.queryServices,
      {
        params: {
          page: pageParams.current,
          size: pageParams.pageSize,
          ...searchParams,
          tabKey: null,
        },
      }
    )
      .then((res) => {
        handleResponse(res, (res) => {
          // 获得真正的总数，要查询条件都为空时
          let obj = {...searchParams}
          delete obj.tabKey
          let arr = Object.values(obj).filter(i=>i)
          if(arr.length == 0){
            setTotal(res.data.count)
          }
          setDataSource(res.data.results);
          setPagination({
            ...pagination,
            total: res.data.count,
            pageSize: pageParams.pageSize,
            current: pageParams.current,
            searchParams: searchParams,
          });
        });
      })
      .catch((e) => console.log(e))
      .finally(() => {
        location.state = {};
        setLoading(false);
        fetchSearchlist();
        //fetchIPlist();
      });
  }

  const fetchSearchlist = () => {
    //setSearchLoading(true);
    fetchGet(apiRequest.appStore.queryLabels, {
      params: {
        label_type: tabKey == "component" ? 0 : 1,
      },
    })
      .then((res) => {
        handleResponse(res, (res) => {
          setSearchData(res.data);
        });
      })
      .catch((e) => console.log(e))
      .finally(() => {
        //setSearchLoading(false);
      });
  };

  useEffect(() => {
    fetchData(
      { current: 1, pageSize: pagination.pageSize },
      {
        ...pagination.searchParams,
        tabKey: tabKey,
        type: searchKey == "全部" ? null : searchKey,
      }
    );
  }, [tabKey, searchKey]);

  return (
    <div>
      <div className={styles.header}>
        <div className={styles.headerTabRow}>
          <div
            className={styles.headerTab}
            onClick={(e) => {
              setPagination({
                current: 1,
                pageSize: viewHeight > 955 ? 12 : 8,
                total: 0,
                searchParams: {},
              });
              setSearchName("");
              setSearchKey("全部");
              if (e.target.innerHTML == "应用服务") {
                setTabKey("service");
              } else if (e.target.innerHTML == "基础组件") {
                setTabKey("component");
              }
            }}
          >
            <div
              style={
                tabKey == "component" ? { color: "rgb(46, 124, 238)" } : {}
              }
            >
              基础组件
            </div>
            <div>|</div>
            <div
              style={tabKey == "service" ? { color: "rgb(46, 124, 238)" } : {}}
            >
              应用服务
            </div>
          </div>
          <div className={styles.headerBtn}>
            <Input
              placeholder="请输入应用名称"
              suffix={
                !searchName && <SearchOutlined style={{ color: "#b6b6b6" }} />
              }
              style={{ marginRight: 10 }}
              value={searchName}
              allowClear
              onChange={(e) => {
                setSearchName(e.target.value);
                if (!e.target.value) {
                  fetchData(
                    {
                      current: 1,
                      pageSize: 10,
                    },
                    {
                      ...pagination.searchParams,
                      [tabKey=="component"?"app_name":"pro_name"]: null,
                    }
                  );
                }
              }}
              onBlur={() => {
                fetchData(
                  {
                    current: 1,
                    pageSize: 10,
                  },
                  {
                    ...pagination.searchParams,
                    [tabKey=="component"?"app_name":"pro_name"]: searchName,
                  }
                );
              }}
              onPressEnter={() => {
                fetchData(
                  {
                    current: 1,
                    pageSize: 10,
                  },
                  {
                    ...pagination.searchParams,
                    [tabKey=="component"?"app_name":"pro_name"]: searchName,
                  }
                );
              }}
            />
            <Button style={{ marginRight: 10 }} type="primary">
              发布
            </Button>
            <Button type="primary">扫描服务端</Button>
          </div>
        </div>

        <hr className={styles.headerHr} />
        <div className={styles.headerSearch}>
          <div
            className={styles.headerSearchCondition}
            onClick={(e) => {
              if (
                searchData?.indexOf(e.target.innerHTML) !== -1 ||
                e.target.innerHTML == "全部"
              ) {
                setSearchKey(e.target.innerHTML);
              }
            }}
          >
            <p
              style={searchKey == "全部" ? { color: "rgb(46, 124, 238)" } : {}}
            >
              全部
            </p>
            {searchData.map((item) => {
              return (
                <p
                  style={
                    searchKey == item ? { color: "rgb(46, 124, 238)" } : {}
                  }
                  key={item}
                >
                  {item}
                </p>
              );
            })}
          </div>
          <div className={styles.headerSearchInfo}>
            <Button
              style={{ marginRight: 15, fontSize: 13 }}
              icon={<DownloadOutlined />}
            >
              <span style={{ color: "#818181" }}>下载组件模版</span>
            </Button>
            共收录 {total} 个{tabKey == "component" ? "基础组件" : "应用服务"}
          </div>
        </div>
      </div>
      <Spin spinning={loading}>
        <div style={{ display: "flex", flexWrap: "wrap" }}>
          {dataSource.length == 0 ? (
            <Empty
              style={{
                width: "100%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                height: viewHeight > 955 ? 500 : 300,
                flexDirection: "column",
              }}
              description={
                tabKey == "component" ? "商店暂无基础组件" : "商店暂无应用服务"
              }
            />
          ) : (
            <>
              {dataSource.map((item, idx) => {
                return (
                  <Card
                    history={history}
                    key={idx}
                    idx={idx + 1}
                    info={item}
                    tabKey={tabKey}
                  />
                );
              })}
            </>
          )}
        </div>
      </Spin>
      {dataSource.length !== 0 && (
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            position: "relative",
            top: 25,
          }}
        >
          <Pagination
            onChange={(e) => {
              fetchData(
                { ...pagination, current: e },
                {
                  ...pagination.searchParams,
                }
              );
            }}
            current={pagination.current}
            pageSize={pagination.pageSize}
            total={pagination.total}
          />
        </div>
      )}
    </div>
  );
};

export default AppStore;