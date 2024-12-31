<?php
class xmlParser {
	public $parser;
	public $depth=0;
	public $termStack;
	public $nodeData;
	public $fullParseData;
	public $prevdepth;
	public $uri;
	public $last_node;
	public $inside_data;
	public $result;
	
	function XmlParser($uri){
		$this->setURI($uri);
		$this->run();
	}

	function run(){
		$this->termStack = array();
		$this->xmlInit();
		if($this->parsing() == 0){
			$this->result = false;
		}else{
			$this->result = true;
		}
	}

	function setURI($uri){
		$this->uri = $uri;
	}

	function xmlInit(){
		$this->result = false;
		$this->parser = xml_parser_create(); 
		if($this->parser){
			if(xml_set_object($this->parser, $this)){
				if(xml_set_element_handler($this->parser, "tag_open", "tag_close")){
					if(xml_set_character_data_handler($this->parser, "cdata")){
						$this->result = true;
					}
				}
			}
		}
	}
	
	function cdata($parser, $cdata){
		if($this->depth > $this->prevdepth){
			if($this->inside_data){
				$this->nodeData[$this->nodeName()] .= $cdata;
			}else{
				$this->nodeData[$this->nodeName()] = $cdata;
			}
			$this->last_node = $this->nodeName();
		}
		$this->inside_data = true;
	}

	function getData($node=null){
		if($node == null){
			return $this->fullParseData;
		}
		return $this->fullParseData[$node];
	}

	function parsing(){
		$fp = @fopen($this->uri, "r");
		if(!$fp){
			return 0;
		}
		while($data = fread($fp, 9182)){
			$this->parse($data);
		}
		fclose($fp);
		return 1;
	}

	function parse($data){
		if(!xml_parse($this->parser, $data)) echo xml_error_string(xml_get_error_code($this->parser));
	}

	function getpNode($depth=0){
		if($depth != 0){
			$node = count($this->termStack) + $depth;
			$stack = array_slice($this->termStack, 0, $node);
		}else{
			$stack = $this->termStack;
		}
		return join("/", $stack);
	}

	function pushStack($name){
		array_push($this->termStack, $name);
	}

	function getStackSize(){
		return count($this->termStack);
	}

	function tag_open($parser, $tag, $attributes){
		$this->pushStack($tag);
		if($this->depth > $this->prevdepth){
			if(count($this->nodeData)){
				$last_node = $this->getpNode(-2);
				$this->fullParseData[$last_node] = $this->nodeData;
			}
			$this->nodeData = array();
			$this->prevdepth = $this->depth;
		}
		$this->depth++;
		$this->inside_data = false;
	}

	function tag_close($parser, $tag){
		$count = count($this->nodeData);
		if($count == 0){
			array_pop($this->termStack);
		}
		$this->depth--;
		if($this->depth < $this->prevdepth){
			if(count($this->nodeData) > 1){
				$this->fullParseData[$this->getpNode()][] = $this->nodeData;
			}else{
				$this->fullParseData[$this->getpNode()] = $this->nodeData;
			}
			$this->nodeData = array();
		}else{
			$this->prevdepth = $this->depth;
		}
		if($count != 0){
			array_pop($this->termStack);
		}
		$this->inside_data = false;
	}

	function nodeName(){
		return $this->termStack[$this->depth-1];
	}
}
?>